/**
 * Web Speech API TTS 컨트롤러
 * Chrome 15초 버그 대응: 문장 단위 청킹
 */
class TTSController {
  constructor() {
    this.synth = window.speechSynthesis;
    this.sections = [];
    this.currentSectionIndex = 0;
    this.rate = 1.0;
    this.voice = null;
    this.isPlaying = false;
    this.isPaused = false;
    this._chunks = [];
    this._chunkIndex = 0;
    this._onStatusChange = null;
    this._progressKey = null;

    this._initVoice();
  }

  /**
   * localStorage 진행 저장용 키를 설정한다.
   * @param {string} key - 예: 'tts-progress:practice-of-presence:1'
   */
  setProgressKey(key) {
    this._progressKey = key;
  }

  /** 현재 재생 위치를 localStorage에 저장한다. */
  saveProgress() {
    if (!this._progressKey || this.sections.length === 0) return;
    var data = {
      sectionIndex: this.currentSectionIndex,
      chunkIndex: this._chunkIndex,
      rate: this.rate,
      sectionLabel: this.sections[this.currentSectionIndex]?.label || '',
      timestamp: Date.now()
    };
    try {
      localStorage.setItem(this._progressKey, JSON.stringify(data));
    } catch (e) { /* quota 초과 등 무시 */ }
  }

  /** 저장된 진행 상태를 삭제한다. */
  clearProgress() {
    if (this._progressKey) {
      localStorage.removeItem(this._progressKey);
    }
  }

  /**
   * 저장된 진행 상태를 읽는다.
   * @param {string} key
   * @returns {{sectionIndex:number, chunkIndex:number, rate:number, sectionLabel:string, timestamp:number}|null}
   */
  static getSavedProgress(key) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  /**
   * 특정 섹션/청크 위치부터 재생을 시작한다.
   */
  playFrom(sectionIndex, chunkIndex) {
    if (this.sections.length === 0) return;
    sectionIndex = Math.min(sectionIndex, this.sections.length - 1);
    this.isPlaying = true;
    this.currentSectionIndex = sectionIndex;
    var section = this.sections[sectionIndex];
    this._emitStatus('재생 중: ' + section.label);
    this._chunks = this._splitToChunks(section.text);
    this._chunkIndex = Math.min(chunkIndex, this._chunks.length - 1);
    this._playNextChunk();
  }

  _initVoice() {
    this._voicesReady = false;
    this._onVoicesReady = null;

    const loadVoices = () => {
      const voices = this.synth.getVoices();
      if (voices.length === 0) return;
      this._voicesReady = true;

      // 저장된 선호 보이스 복원
      var savedUri = this._loadVoicePref();
      if (savedUri) {
        var match = voices.find(v => v.voiceURI === savedUri);
        if (match) { this.voice = match; }
      }

      // 선호 보이스가 없으면 유나 > Google 한국어 > 한국어 기본값
      if (!this.voice) {
        var nameLC;
        this.voice = voices.find(v => { nameLC = v.name.toLowerCase(); return nameLC.indexOf('yuna') !== -1; })
          || voices.find(v => { nameLC = v.name.toLowerCase(); return nameLC.indexOf('google') !== -1 && v.lang.startsWith('ko'); })
          || voices.find(v => v.lang.startsWith('ko'))
          || voices[0] || null;
      }

      if (this._onVoicesReady) this._onVoicesReady();
    };

    loadVoices();
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = loadVoices;
    }
  }

  /**
   * 사용 가능한 보이스 목록을 반환한다.
   * @param {string} [langFilter] - 언어 필터 (예: 'ko'). 생략 시 전체 반환.
   * @returns {SpeechSynthesisVoice[]}
   */
  getVoices(langFilter) {
    var voices = this.synth.getVoices();
    if (langFilter) {
      voices = voices.filter(v => v.lang.startsWith(langFilter));
    }
    return voices;
  }

  /**
   * 보이스를 변경하고 localStorage에 저장한다.
   * @param {string} voiceURI - SpeechSynthesisVoice.voiceURI
   */
  setVoice(voiceURI) {
    var voices = this.synth.getVoices();
    var match = voices.find(v => v.voiceURI === voiceURI);
    if (match) {
      this.voice = match;
      this._saveVoicePref(voiceURI);
      // 재생 중이면 현재 위치에서 재시작
      if (this.isPlaying && !this.isPaused) {
        var secIdx = this.currentSectionIndex;
        var chkIdx = this._chunkIndex;
        this.stop();
        this.isPlaying = true;
        this.currentSectionIndex = secIdx;
        var section = this.sections[secIdx];
        this._emitStatus('재생 중: ' + section.label);
        this._chunks = this._splitToChunks(section.text);
        this._chunkIndex = chkIdx;
        this._playNextChunk();
      }
    }
  }

  /**
   * 보이스가 로드되면 콜백을 호출한다.
   * 이미 로드된 상태면 즉시 호출.
   */
  onVoicesReady(callback) {
    if (this._voicesReady) { callback(); return; }
    this._onVoicesReady = callback;
  }

  _saveVoicePref(voiceURI) {
    try { localStorage.setItem('tts-voice-pref', voiceURI); } catch (e) {}
  }

  _loadVoicePref() {
    try { return localStorage.getItem('tts-voice-pref'); } catch (e) { return null; }
  }

  onStatusChange(callback) {
    this._onStatusChange = callback;
  }

  _emitStatus(msg) {
    if (this._onStatusChange) this._onStatusChange(msg);
  }

  /**
   * 읽을 섹션들을 등록한다.
   * @param {Array<{label: string, text: string}>} sections
   */
  setSections(sections) {
    this.stop();
    this.sections = sections;
    this.currentSectionIndex = 0;
  }

  /**
   * 텍스트를 문장 단위로 분할한다 (Chrome 15초 버그 대응).
   */
  _splitToChunks(text) {
    // 한국어 문장 분리: 마침표, 느낌표, 물음표 뒤에서 분할
    const sentences = text.match(/[^.!?]*[.!?]+[\s]*/g) || [text];
    return sentences.map(s => s.trim()).filter(s => s.length > 0);
  }

  /**
   * 현재 섹션부터 재생을 시작한다.
   */
  play() {
    if (this.sections.length === 0) return;

    if (this.isPaused) {
      this.synth.resume();
      this.isPaused = false;
      this.isPlaying = true;
      this._emitStatus('재생 중: ' + this.sections[this.currentSectionIndex].label);
      return;
    }

    this.isPlaying = true;
    this._playSection(this.currentSectionIndex);
  }

  _playSection(index) {
    if (index >= this.sections.length) {
      this.isPlaying = false;
      this.clearProgress();
      this._emitStatus('재생 완료');
      return;
    }

    this.currentSectionIndex = index;
    const section = this.sections[index];
    this._emitStatus('재생 중: ' + section.label);

    this._chunks = this._splitToChunks(section.text);
    this._chunkIndex = 0;
    this._playNextChunk();
  }

  _playNextChunk() {
    if (!this.isPlaying) return;
    if (this._chunkIndex >= this._chunks.length) {
      // 현재 섹션 완료, 다음 섹션으로
      this._playSection(this.currentSectionIndex + 1);
      return;
    }

    this.saveProgress();

    const utterance = new SpeechSynthesisUtterance(this._chunks[this._chunkIndex]);
    utterance.lang = 'ko-KR';
    utterance.rate = this.rate;
    if (this.voice) utterance.voice = this.voice;

    utterance.onend = () => {
      this._chunkIndex++;
      this._playNextChunk();
    };

    utterance.onerror = (e) => {
      if (e.error === 'interrupted' || e.error === 'cancelled') return;
      console.error('TTS 오류:', e.error);
      this._chunkIndex++;
      this._playNextChunk();
    };

    this.synth.speak(utterance);
  }

  pause() {
    if (!this.isPlaying) return;
    this.synth.pause();
    this.isPaused = true;
    this.saveProgress();
    this._emitStatus('일시정지');
  }

  stop() {
    this.synth.cancel();
    this.isPlaying = false;
    this.isPaused = false;
    this._chunks = [];
    this._chunkIndex = 0;
    this._emitStatus('정지');
  }

  togglePlayPause() {
    if (this.isPlaying && !this.isPaused) {
      this.pause();
    } else {
      this.play();
    }
  }

  prevSection() {
    this.stop();
    this.currentSectionIndex = Math.max(0, this.currentSectionIndex - 1);
    this._emitStatus('섹션: ' + this.sections[this.currentSectionIndex].label);
  }

  nextSection() {
    this.stop();
    this.currentSectionIndex = Math.min(
      this.sections.length - 1,
      this.currentSectionIndex + 1
    );
    this._emitStatus('섹션: ' + this.sections[this.currentSectionIndex].label);
  }

  setRate(rate) {
    this.rate = rate;
    // 재생 중이면 재시작
    if (this.isPlaying && !this.isPaused) {
      const idx = this.currentSectionIndex;
      this.stop();
      this.isPlaying = true;
      this._playSection(idx);
    }
  }
}
