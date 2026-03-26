# Phase 3 확장 카탈로그: 시각장애인을 위한 신앙 고전 660권

> 작성일: 2026-03-25
> 목적: OpenAI API ~$2,000 크레딧으로 처리할 추가 퍼블릭 도메인 신앙 도서 목록
> 상태: 카탈로그만 작성 (실제 처리 작업은 별도 진행)
> 기존 처리 완료: ~398권 (faith-book-catalog.md + faith-book-catalog-expanded.md 참조)

---

## 예산 요약

| 항목 | 수량 | 예상 비용 |
|------|------|-----------|
| Phase 1 처리 완료 | 58권 | ~$140 (완료) |
| Phase 2 처리 완료 | 340권 | ~$1,020 (완료) |
| **Phase 3 신규 대상** | **660권** | **~$2,000** |
| 누적 총계 | 1,058권 | ~$3,160 |

- 평균 처리 비용: 권당 ~$3 (gpt Batch API, 챕터 수에 따라 $0.50~$8 변동)
- 소스: Project Gutenberg, CCEL, Internet Archive, Wikisource, NewAdvent
- 번호: #341부터 시작 (Phase 2 카탈로그 #340 이후)

---

## 카테고리 14: 교회사 텍스트 — 40권

> 초대교회부터 근대까지의 교회사 기록과 역사 서술

### 14A. 고대 교회사 (1~5세기)

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 341 | eusebius-church-history | Church History | 교회사 | Eusebius of Caesarea | 339 | 25 | CCEL (NPNF2 Vol.1) |
| 342 | eusebius-life-constantine | Life of Constantine | 콘스탄티누스의 생애 | Eusebius of Caesarea | 339 | 15 | CCEL (NPNF2 Vol.1) |
| 343 | eusebius-martyrs-palestine | Martyrs of Palestine | 팔레스타인 순교자들 | Eusebius of Caesarea | 339 | 10 | CCEL (NPNF2 Vol.1) |
| 344 | socrates-church-history | Church History | 교회사 | Socrates Scholasticus | ~439 | 20 | CCEL (NPNF2 Vol.2) |
| 345 | sozomen-church-history | Church History | 교회사 | Sozomen | ~450 | 20 | CCEL (NPNF2 Vol.2) |
| 346 | theodoret-church-history | Church History | 교회사 | Theodoret | 457 | 15 | CCEL (NPNF2 Vol.3) |
| 347 | theodoret-religious-history | Religious History | 수도사 열전 | Theodoret | 457 | 15 | CCEL (NPNF2 Vol.3) |
| 348 | sulpicius-life-martin | Life of St. Martin | 성 마르틴의 생애 | Sulpicius Severus | ~425 | 8 | CCEL (NPNF2 Vol.11) |
| 349 | sulpicius-sacred-history | Sacred History | 거룩한 역사 | Sulpicius Severus | ~425 | 12 | CCEL / Archive |

### 14B. 중세 교회사

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 350 | bede-ecclesiastical-history | Ecclesiastical History of the English People | 영국민의 교회사 | Venerable Bede | 735 | 20 | Gutenberg / CCEL |
| 351 | adam-bremen-history | History of the Archbishops of Hamburg-Bremen (sel.) | 함부르크-브레멘 대주교사 (선집) | Adam of Bremen | ~1081 | 10 | Archive |
| 352 | william-malmesbury-gesta | Gesta Regum Anglorum (selections) | 잉글랜드 왕들의 행적 (선집) | William of Malmesbury | 1143 | 12 | Archive / Gutenberg |

### 14C. 종교개혁기 교회사

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 353 | daubigne-reformation-v1 | History of the Reformation Vol.1 | 종교개혁사 제1권 | J.H. Merle d'Aubigné | 1872 | 20 | Gutenberg |
| 354 | daubigne-reformation-v2 | History of the Reformation Vol.2 | 종교개혁사 제2권 | J.H. Merle d'Aubigné | 1872 | 20 | Gutenberg |
| 355 | daubigne-reformation-v3 | History of the Reformation Vol.3 | 종교개혁사 제3권 | J.H. Merle d'Aubigné | 1872 | 20 | Gutenberg |
| 356 | daubigne-reformation-v4 | History of the Reformation Vol.4 | 종교개혁사 제4권 | J.H. Merle d'Aubigné | 1872 | 20 | Gutenberg |
| 357 | daubigne-reformation-v5 | History of the Reformation Vol.5 | 종교개혁사 제5권 | J.H. Merle d'Aubigné | 1872 | 20 | Gutenberg |
| 358 | motley-dutch-republic-sel | Rise of the Dutch Republic (selections) | 네덜란드 공화국의 흥기 (선집) | John Lothrop Motley | 1877 | 20 | Gutenberg |
| 359 | wylie-history-protestantism-v1 | History of Protestantism Vol.1 | 개신교 역사 제1권 | J.A. Wylie | 1890 | 20 | Archive / Gutenberg |
| 360 | wylie-history-protestantism-v2 | History of Protestantism Vol.2 | 개신교 역사 제2권 | J.A. Wylie | 1890 | 20 | Archive / Gutenberg |
| 361 | wylie-history-protestantism-v3 | History of Protestantism Vol.3 | 개신교 역사 제3권 | J.A. Wylie | 1890 | 20 | Archive / Gutenberg |

### 14D. 근대 교회사

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 362 | schaff-history-v1 | History of the Christian Church Vol.1: Apostolic | 기독교 교회사 제1권: 사도시대 | Philip Schaff | 1893 | 20 | CCEL |
| 363 | schaff-history-v2 | History of the Christian Church Vol.2: Ante-Nicene | 기독교 교회사 제2권: 니케아 이전 | Philip Schaff | 1893 | 20 | CCEL |
| 364 | schaff-history-v3 | History of the Christian Church Vol.3: Nicene | 기독교 교회사 제3권: 니케아 | Philip Schaff | 1893 | 20 | CCEL |
| 365 | schaff-history-v4 | History of the Christian Church Vol.4: Medieval | 기독교 교회사 제4권: 중세 | Philip Schaff | 1893 | 20 | CCEL |
| 366 | schaff-history-v5 | History of the Christian Church Vol.5: Middle Ages | 기독교 교회사 제5권: 중세후기 | Philip Schaff | 1893 | 20 | CCEL |
| 367 | schaff-history-v6 | History of the Christian Church Vol.6: Reformation | 기독교 교회사 제6권: 종교개혁 | Philip Schaff | 1893 | 20 | CCEL |
| 368 | schaff-history-v7 | History of the Christian Church Vol.7: Swiss Reformation | 기독교 교회사 제7권: 스위스 종교개혁 | Philip Schaff | 1893 | 20 | CCEL |
| 369 | schaff-history-v8 | History of the Christian Church Vol.8: Modern | 기독교 교회사 제8권: 근대 | Philip Schaff | 1893 | 20 | CCEL |
| 370 | latourette-missions-sel | History of the Expansion of Christianity (sel.) | 기독교 확장사 (선집) | K.S. Latourette | 1968 | 20 | Archive |
| 371 | kurtz-church-history | Church History (selections) | 교회사 (선집) | Johann Heinrich Kurtz | 1890 | 20 | Archive / Gutenberg |
| 372 | neander-church-history-sel | General History of the Christian Religion (sel.) | 기독교 통사 (선집) | Augustus Neander | 1850 | 20 | Archive |
| 373 | milman-latin-christianity-sel | History of Latin Christianity (selections) | 라틴 기독교 역사 (선집) | Henry Hart Milman | 1868 | 15 | Archive / Gutenberg |
| 374 | fisher-history-reformation | History of the Reformation | 종교개혁사 | George Park Fisher | 1909 | 15 | Archive / Gutenberg |
| 375 | harnack-expansion-sel | The Mission and Expansion of Christianity (sel.) | 기독교 선교와 확장 (선집) | Adolf von Harnack | 1930 | 15 | Archive |
| 376 | robertson-history-church-sel | History of the Christian Church (selections) | 기독교회사 (선집) | James C. Robertson | 1882 | 15 | Archive |
| 377 | stanley-eastern-church | Lectures on the History of the Eastern Church | 동방교회사 강의 | Arthur P. Stanley | 1881 | 15 | Archive / Gutenberg |
| 378 | waddington-church-history-sel | A History of the Church (selections) | 교회사 (선집) | George Waddington | 1869 | 12 | Archive |
| 379 | broadus-history-preaching | History of Preaching | 설교사 | John A. Broadus | 1895 | 15 | Archive |
| 380 | killen-ancient-church | The Ancient Church | 고대 교회 | W.D. Killen | 1902 | 15 | Archive |

**소계**: 40권, ~670챕터, 예상 비용 ~$120

---

## 카테고리 15: 동방교회 & 정교회 전통 — 30권

> 사막 교부, 동방 신비주의, 정교회 영성 전통

### 15A. 사막 교부 & 수도원 전통

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 381 | sayings-desert-fathers | Sayings of the Desert Fathers (Apophthegmata) | 사막 교부들의 금언 | Various | 4~5C | 20 | CCEL / Archive |
| 382 | desert-mothers-sel | Sayings of the Desert Mothers (selections) | 사막 어머니들의 금언 (선집) | Various | 4~5C | 10 | Archive |
| 383 | john-climacus-ladder | The Ladder of Divine Ascent | 신적 상승의 사다리 | John Climacus | 606 | 20 | CCEL / Archive |
| 384 | evagrius-praktikos | The Praktikos and Chapters on Prayer | 실천론과 기도의 장들 | Evagrius Ponticus | 399 | 12 | Archive |
| 385 | dorotheos-gaza-instructions | Instructions (Spiritual Teaching) | 영적 가르침 | Dorotheos of Gaza | ~560 | 12 | Archive |
| 386 | palladius-lausiac-history | Lausiac History | 라우시아 교부전 | Palladius | ~431 | 15 | CCEL / Archive |
| 387 | isaac-syrian-homilies-sel | Ascetical Homilies (selections) | 금욕적 강론 (선집) | Isaac the Syrian | ~700 | 15 | Archive |
| 388 | pachomius-rules | Rules and Life of Pachomius | 파코미우스 규칙서와 생애 | Pachomius | 346 | 10 | Archive / CCEL |

### 15B. 동방 신학자

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 389 | maximus-confessor-centuries | Centuries on Love | 사랑에 관한 백 장 | Maximus the Confessor | 662 | 10 | Archive |
| 390 | maximus-confessor-ambigua-sel | Ambigua (selections) | 난해 구절 해설 (선집) | Maximus the Confessor | 662 | 12 | Archive |
| 391 | symeon-new-theologian-sel | Discourses (selections) | 담론 (선집) | Symeon the New Theologian | 1022 | 15 | Archive |
| 392 | gregory-palamas-triads-sel | Triads in Defence of the Holy Hesychasts (sel.) | 거룩한 정적주의자 옹호 삼부작 (선집) | Gregory Palamas | 1359 | 12 | Archive |
| 393 | ephrem-syrian-hymns-sel | Hymns on Paradise and Selected Hymns | 낙원 찬송과 기타 선집 | Ephrem the Syrian | 373 | 15 | CCEL (NPNF2 Vol.13) |
| 394 | cyril-jerusalem-catechetical | Catechetical Lectures | 교리교육 강의 | Cyril of Jerusalem | 386 | 20 | CCEL (NPNF2 Vol.7) |
| 395 | cyril-alex-on-john-sel | Commentary on John (selections) | 요한복음 주석 (선집) | Cyril of Alexandria | 444 | 15 | Archive / CCEL |
| 396 | dionysius-areopagite-full | Complete Works (Celestial/Eccl. Hierarchies) | 전집 (천상/교회 위계론) | Pseudo-Dionysius | ~500 | 12 | CCEL / Archive |

### 15C. 러시아 & 슬라브 영성

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 397 | way-of-pilgrim | The Way of a Pilgrim | 순례자의 길 | Anonymous | 19C | 12 | Gutenberg / Archive |
| 398 | philokalia-sel-v1 | Philokalia Vol.1 (selections) | 필로칼리아 제1권 (선집) | Various | 4~15C | 20 | Archive |
| 399 | philokalia-sel-v2 | Philokalia Vol.2 (selections) | 필로칼리아 제2권 (선집) | Various | 4~15C | 20 | Archive |
| 400 | theophan-recluse-prayer | The Art of Prayer | 기도의 예술 | Theophan the Recluse | 1894 | 15 | Archive |
| 401 | theophan-recluse-path | The Path to Salvation | 구원의 길 | Theophan the Recluse | 1894 | 15 | Archive |
| 402 | tikhon-zadonsk-sel | Selected Spiritual Writings | 영적 저작 선집 | Tikhon of Zadonsk | 1783 | 12 | Archive |
| 403 | john-kronstadt-my-life | My Life in Christ (selections) | 그리스도 안의 나의 삶 (선집) | John of Kronstadt | 1908 | 15 | Archive |
| 404 | ignatius-brianchaninov-sel | The Arena: Guidelines for Spiritual Life | 영적 투기장 | Ignatius Brianchaninov | 1867 | 15 | Archive |
| 405 | nil-sorsky-tradition | The Tradition of the Skit (selections) | 수도 전통 (선집) | Nil Sorsky | 1508 | 8 | Archive |
| 406 | optina-elders-sel | Writings of the Optina Elders (selections) | 옵티나 수도원 장로들의 글 (선집) | Various | 19C | 12 | Archive |
| 407 | russian-primary-chronicle-sel | Russian Primary Chronicle: Christian sections | 러시아 원초 연대기: 기독교 관련 부분 | Nestor | ~1113 | 10 | Archive |
| 408 | seraphim-sarov-conversations | Conversation with Motovilov | 모토빌로프와의 대화 | Seraphim of Sarov | 1833 | 8 | Archive |
| 409 | paisius-velichkovsky-sel | Selected Writings | 저작 선집 | Paisius Velichkovsky | 1794 | 8 | Archive |
| 410 | hesychius-jerusalem-sel | On Watchfulness and Holiness | 경성과 거룩에 관하여 | Hesychius of Jerusalem | ~450 | 8 | Archive |

**소계**: 30권, ~392챕터, 예상 비용 ~$90

---

## 카테고리 16: 기독교 소설 & 알레고리 — 25권

> 신앙적 주제를 담은 퍼블릭 도메인 문학 작품

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 411 | macdonald-phantastes | Phantastes | 판타스테스 | George MacDonald | 1905 | 20 | Gutenberg |
| 412 | macdonald-lilith | Lilith | 릴리스 | George MacDonald | 1905 | 20 | Gutenberg |
| 413 | macdonald-princess-goblin | The Princess and the Goblin | 공주와 고블린 | George MacDonald | 1905 | 20 | Gutenberg |
| 414 | macdonald-princess-curdie | The Princess and Curdie | 공주와 커디 | George MacDonald | 1905 | 15 | Gutenberg |
| 415 | macdonald-at-back-north-wind | At the Back of the North Wind | 북풍의 등 뒤에서 | George MacDonald | 1905 | 20 | Gutenberg |
| 416 | macdonald-robert-falconer | Robert Falconer | 로버트 팔코너 | George MacDonald | 1905 | 20 | Gutenberg |
| 417 | macdonald-sir-gibbie | Sir Gibbie | 기비 경 | George MacDonald | 1905 | 20 | Gutenberg |
| 418 | sheldon-in-his-steps | In His Steps | 예수님이라면 어떻게 하실까 | Charles M. Sheldon | 1946 | 15 | Gutenberg |
| 419 | sheldon-crucifixion-philip-strong | The Crucifixion of Philip Strong | 필립 스트롱의 십자가 | Charles M. Sheldon | 1946 | 15 | Gutenberg |
| 420 | lew-wallace-ben-hur | Ben-Hur: A Tale of the Christ | 벤허: 그리스도 이야기 | Lew Wallace | 1905 | 20 | Gutenberg |
| 421 | sienkiewicz-quo-vadis | Quo Vadis | 쿠오 바디스 | Henryk Sienkiewicz | 1916 | 20 | Gutenberg |
| 422 | kingsley-hypatia | Hypatia | 히파티아 | Charles Kingsley | 1875 | 20 | Gutenberg |
| 423 | kingsley-westward-ho-sel | Westward Ho! (selections) | 서쪽으로! (선집) | Charles Kingsley | 1875 | 15 | Gutenberg |
| 424 | yonge-heir-redclyffe | The Heir of Redclyffe | 레드클리프의 상속인 | Charlotte M. Yonge | 1901 | 20 | Gutenberg |
| 425 | yonge-daisy-chain | The Daisy Chain | 데이지 체인 | Charlotte M. Yonge | 1901 | 20 | Gutenberg |
| 426 | ingraham-prince-house-david | The Prince of the House of David | 다윗 집의 왕자 | J.H. Ingraham | 1860 | 15 | Gutenberg |
| 427 | elizabeth-charles-chronicles-schonberg | Chronicles of the Schönberg-Cotta Family | 쇤베르크-코타 가문 연대기 | Elizabeth Rundle Charles | 1896 | 15 | Gutenberg / Archive |
| 428 | phelps-gates-ajar | The Gates Ajar | 열린 문 | Elizabeth Stuart Phelps | 1911 | 12 | Gutenberg |
| 429 | mulock-john-halifax | John Halifax, Gentleman | 신사 존 핼리팩스 | Dinah Mulock Craik | 1887 | 20 | Gutenberg |
| 430 | corelli-barabbas | Barabbas: A Dream of the World's Tragedy | 바라바 | Marie Corelli | 1924 | 15 | Gutenberg / Archive |
| 431 | shorthouse-john-inglesant | John Inglesant | 존 잉글샌트 | J.H. Shorthouse | 1903 | 20 | Archive / Gutenberg |
| 432 | wiseman-fabiola | Fabiola, or the Church of the Catacombs | 파비올라: 지하묘지의 교회 | Cardinal Wiseman | 1865 | 15 | Gutenberg |
| 433 | newman-callista | Callista: A Tale of the Third Century | 칼리스타: 3세기 이야기 | John Henry Newman | 1890 | 15 | Gutenberg |
| 434 | edersheim-sketches-jewish | Sketches of Jewish Social Life | 유대인의 사회생활 단상 | Alfred Edersheim | 1889 | 15 | Gutenberg / CCEL |
| 435 | bunyan-badman | The Life and Death of Mr. Badman | 배드맨의 생과 사 | John Bunyan | 1688 | 12 | Gutenberg / CCEL |

**소계**: 25권, ~419챕터, 예상 비용 ~$75

---

## 카테고리 17: 기독교 윤리 & 사회사상 — 20권

> 기독교 사회 윤리, 사회복음, 기독교적 사회 개혁 문헌

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 436 | wilberforce-practical-christianity | A Practical View of Christianity | 기독교의 실제적 관점 | William Wilberforce | 1833 | 15 | Gutenberg |
| 437 | wilberforce-abolition-slave-trade | Letter on the Abolition of the Slave Trade | 노예무역 폐지에 관한 서신 | William Wilberforce | 1833 | 10 | Archive / Gutenberg |
| 438 | rauschenbusch-christianity-social-crisis | Christianity and the Social Crisis | 기독교와 사회 위기 | Walter Rauschenbusch | 1918 | 15 | Archive / Gutenberg |
| 439 | rauschenbusch-theology-social-gospel | A Theology for the Social Gospel | 사회복음을 위한 신학 | Walter Rauschenbusch | 1918 | 15 | Archive |
| 440 | gladden-applied-christianity | Applied Christianity | 응용 기독교 | Washington Gladden | 1918 | 12 | Archive |
| 441 | gladden-social-salvation | Social Salvation | 사회적 구원 | Washington Gladden | 1918 | 12 | Archive |
| 442 | strong-josiah-our-country | Our Country | 우리의 나라 | Josiah Strong | 1916 | 12 | Archive / Gutenberg |
| 443 | mathews-social-teaching-jesus | The Social Teaching of Jesus | 예수의 사회적 가르침 | Shailer Mathews | 1941 | 12 | Archive |
| 444 | peabody-jesus-christ-social-question | Jesus Christ and the Social Question | 예수 그리스도와 사회문제 | Francis Greenwood Peabody | 1936 | 12 | Archive / Gutenberg |
| 445 | kuyper-lectures-calvinism | Lectures on Calvinism (Stone Lectures) | 칼빈주의 강연 | Abraham Kuyper | 1920 | 10 | CCEL / Archive |
| 446 | kuyper-work-holy-spirit-sel | The Work of the Holy Spirit (selections) | 성령의 사역 (선집) | Abraham Kuyper | 1920 | 15 | Archive |
| 447 | maurice-kingdom-christ-sel | The Kingdom of Christ (selections) | 그리스도의 나라 (선집) | F.D. Maurice | 1872 | 15 | Archive |
| 448 | gore-lux-mundi-sel | Lux Mundi (selections) | 세계의 빛 (선집) | Charles Gore (ed.) | 1932 | 12 | Archive |
| 449 | ritschl-justification-sel | Justification and Reconciliation (selections) | 칭의와 화해 (선집) | Albrecht Ritschl | 1889 | 12 | Archive |
| 450 | forsyth-work-of-christ | The Work of Christ | 그리스도의 사역 | P.T. Forsyth | 1921 | 12 | Archive |
| 451 | forsyth-positive-preaching | Positive Preaching and the Modern Mind | 적극적 설교와 현대 정신 | P.T. Forsyth | 1921 | 12 | Archive |
| 452 | ely-social-aspects-christianity | Social Aspects of Christianity | 기독교의 사회적 측면 | Richard T. Ely | 1943 | 10 | Archive |
| 453 | headlam-christian-theology | Christian Theology: The Doctrine of God | 기독교 신학: 하나님의 교리 | A.C. Headlam | 1947 | 12 | Archive |
| 454 | drummond-natural-law | Natural Law in the Spiritual World | 영적 세계의 자연 법칙 | Henry Drummond | 1897 | 15 | Gutenberg / CCEL |
| 455 | drummond-greatest-thing | The Greatest Thing in the World | 세상에서 가장 위대한 것 | Henry Drummond | 1897 | 8 | Gutenberg / CCEL |

**소계**: 20권, ~248챕터, 예상 비용 ~$60

---

## 카테고리 18: 목회신학 & 사역 지침서 — 25권

> 목회 실천, 영혼 돌봄, 교회 사역에 관한 고전

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 456 | bridges-christian-ministry | The Christian Ministry | 기독교 사역론 | Charles Bridges | 1869 | 15 | Archive / CCEL |
| 457 | baxter-dying-thoughts | Dying Thoughts | 임종의 묵상 | Richard Baxter | 1691 | 10 | CCEL |
| 458 | baxter-saints-rest-full | The Saints' Everlasting Rest (expanded) | 성도의 영원한 안식 (확장판) | Richard Baxter | 1691 | 20 | CCEL / Gutenberg |
| 459 | spencer-pastors-sketches | A Pastor's Sketches | 목사의 기록 | Ichabod Spencer | 1854 | 15 | Archive / Gutenberg |
| 460 | spencer-pastors-sketches-v2 | A Pastor's Sketches Vol.2 | 목사의 기록 제2권 | Ichabod Spencer | 1854 | 15 | Archive |
| 461 | fairbairn-pastoral-epistles | Commentary on the Pastoral Epistles | 목회서신 주석 | Patrick Fairbairn | 1874 | 12 | Archive / CCEL |
| 462 | fairbairn-typology | Typology of Scripture | 성경의 예표론 | Patrick Fairbairn | 1874 | 15 | Archive |
| 463 | alexander-james-thoughts-preaching | Thoughts on Preaching | 설교에 대한 생각 | James W. Alexander | 1859 | 12 | Archive |
| 464 | kidder-homiletics | A Treatise on Homiletics | 설교학 논문 | Daniel P. Kidder | 1891 | 12 | Archive |
| 465 | shedd-homiletics | Homiletics and Pastoral Theology | 설교학과 목회신학 | W.G.T. Shedd | 1894 | 15 | Archive |
| 466 | murphy-pastoral-theology | Pastoral Theology | 목회신학 | Thomas Murphy | 1900 | 12 | Archive |
| 467 | vinet-pastoral-theology | Pastoral Theology | 목회신학 | Alexandre Vinet | 1847 | 15 | Archive |
| 468 | oden-care-of-souls-sel | Care of Souls in the Classic Tradition (selections) | 고전적 영혼 돌봄 (선집) | Gregory / Chrysostom | 5C | 12 | CCEL |
| 469 | mcneill-cure-of-souls-sel | A History of the Cure of Souls (selections) | 영혼 치유의 역사 (선집) | Various | — | 12 | Archive |
| 470 | spurgeon-soul-winner | The Soul Winner | 영혼을 이기는 사람 | C.H. Spurgeon | 1892 | 12 | CCEL / Gutenberg |
| 471 | spurgeon-commenting-commentaries | Commenting and Commentaries | 주석과 주석서들 | C.H. Spurgeon | 1892 | 10 | Gutenberg |
| 472 | spurgeon-eccentric-preachers | Eccentric Preachers | 별난 설교자들 | C.H. Spurgeon | 1892 | 10 | Gutenberg |
| 473 | dabney-sacred-rhetoric | Sacred Rhetoric | 거룩한 수사학 | R.L. Dabney | 1898 | 12 | Archive |
| 474 | phelps-men-and-books | Men and Books | 사람과 책 | Austin Phelps | 1890 | 12 | Archive |
| 475 | phelps-theory-of-preaching | The Theory of Preaching | 설교의 이론 | Austin Phelps | 1890 | 15 | Archive |
| 476 | watson-john-cure-of-souls | The Cure of Souls | 영혼의 치유 | John Watson (Ian Maclaren) | 1907 | 12 | Archive |
| 477 | jowett-preacher-his-life | The Preacher: His Life and Work | 설교자: 삶과 사역 | John Henry Jowett | 1923 | 10 | Archive |
| 478 | jefferson-minister-as-shepherd | The Minister as Shepherd | 목자로서의 목사 | Charles E. Jefferson | 1938 | 12 | Archive |
| 479 | oman-concerning-ministry | Concerning the Ministry | 사역에 관하여 | John Oman | 1939 | 10 | Archive |
| 480 | forsyth-soul-of-prayer | The Soul of Prayer | 기도의 영혼 | P.T. Forsyth | 1921 | 10 | Archive |

**소계**: 25권, ~313챕터, 예상 비용 ~$75

---

## 카테고리 19: 성경 배경 & 고고학 — 15권

> 성경 시대의 역사, 문화, 지리, 고고학적 배경

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 481 | edersheim-life-times-jesus-v1 | The Life and Times of Jesus the Messiah Vol.1 | 예수의 생애와 시대 제1권 | Alfred Edersheim | 1889 | 20 | Gutenberg / CCEL |
| 482 | edersheim-life-times-jesus-v2 | The Life and Times of Jesus the Messiah Vol.2 | 예수의 생애와 시대 제2권 | Alfred Edersheim | 1889 | 20 | Gutenberg / CCEL |
| 483 | edersheim-temple-services | The Temple: Its Ministry and Services | 성전: 사역과 예배 | Alfred Edersheim | 1889 | 15 | Gutenberg / CCEL |
| 484 | farrar-life-christ-v1 | The Life of Christ Vol.1 | 그리스도의 생애 제1권 | Frederic W. Farrar | 1903 | 20 | Gutenberg |
| 485 | farrar-life-christ-v2 | The Life of Christ Vol.2 | 그리스도의 생애 제2권 | Frederic W. Farrar | 1903 | 20 | Gutenberg |
| 486 | farrar-life-paul-v1 | The Life and Work of St. Paul Vol.1 | 사도 바울의 생애와 사역 제1권 | Frederic W. Farrar | 1903 | 20 | Gutenberg |
| 487 | farrar-life-paul-v2 | The Life and Work of St. Paul Vol.2 | 사도 바울의 생애와 사역 제2권 | Frederic W. Farrar | 1903 | 20 | Gutenberg |
| 488 | farrar-early-days-christianity | The Early Days of Christianity | 기독교 초기 시대 | Frederic W. Farrar | 1903 | 20 | Gutenberg |
| 489 | conybeare-howson-paul-sel | The Life and Epistles of St. Paul (sel.) | 사도 바울의 생애와 서신 (선집) | Conybeare & Howson | 1905 | 20 | Gutenberg |
| 490 | lightfoot-biblical-essays | Biblical Essays | 성경 에세이 | J.B. Lightfoot | 1889 | 12 | Archive |
| 491 | lightfoot-apostolic-fathers-intro | Introduction to the Apostolic Fathers | 사도교부 서론 | J.B. Lightfoot | 1889 | 12 | Archive / CCEL |
| 492 | ramsay-paul-traveller | St. Paul the Traveller and Roman Citizen | 여행자 바울과 로마 시민 | William M. Ramsay | 1939 | 15 | Archive / Gutenberg |
| 493 | ramsay-church-roman-empire | The Church in the Roman Empire | 로마제국의 교회 | William M. Ramsay | 1939 | 15 | Archive |
| 494 | smith-old-testament-history | Old Testament History | 구약 역사 | Henry Preserved Smith | 1927 | 15 | Archive |
| 495 | josephus-wars-sel | The Wars of the Jews (selections) | 유대 전쟁사 (선집) | Flavius Josephus | ~100 | 20 | Gutenberg |

**소계**: 15권, ~264챕터, 예상 비용 ~$45

---

## 카테고리 20: NPNF/ANF 시리즈 확장 — 60권

> Ante-Nicene Fathers, Nicene & Post-Nicene Fathers 시리즈 미처리 권

### 20A. ANF 확장 (Ante-Nicene Fathers)

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 496 | anf-vol1-justin-remains | ANF Vol.1: Justin Martyr Fragments | ANF 1: 유스티누스 단편집 | Justin Martyr | 165 | 10 | CCEL |
| 497 | anf-vol1-tatian | ANF Vol.1: Tatian's Address to the Greeks | ANF 1: 타티안의 헬라인에게 | Tatian | ~180 | 10 | CCEL |
| 498 | anf-vol1-athenagoras | ANF Vol.1: Athenagoras — Plea & Resurrection | ANF 1: 아테나고라스 — 탄원서와 부활론 | Athenagoras | ~190 | 10 | CCEL |
| 499 | anf-vol2-clement-misc | ANF Vol.2: Clement Misc. Writings | ANF 2: 클레멘트 기타 저작 | Clement of Alexandria | 215 | 12 | CCEL |
| 500 | anf-vol3-tertullian-v2 | ANF Vol.3: Tertullian Part 2 | ANF 3: 테르툴리아누스 제2부 | Tertullian | 220 | 15 | CCEL |
| 501 | anf-vol3-tertullian-v3 | ANF Vol.3: Tertullian Part 3 | ANF 3: 테르툴리아누스 제3부 | Tertullian | 220 | 12 | CCEL |
| 502 | anf-vol4-tertullian-v4 | ANF Vol.4: Tertullian Part 4 | ANF 4: 테르툴리아누스 제4부 | Tertullian | 220 | 12 | CCEL |
| 503 | anf-vol4-minucius-felix | ANF Vol.4: Minucius Felix — Octavius | ANF 4: 미누키우스 펠릭스 — 옥타비우스 | Minucius Felix | ~250 | 8 | CCEL |
| 504 | anf-vol4-commodian | ANF Vol.4: Commodianus Instructions | ANF 4: 코모디아누스 지침서 | Commodianus | ~250 | 8 | CCEL |
| 505 | anf-vol5-hippolytus | ANF Vol.5: Hippolytus — Refutation of Heresies | ANF 5: 히폴리투스 — 이단 반박 | Hippolytus | ~236 | 15 | CCEL |
| 506 | anf-vol5-novatian | ANF Vol.5: Novatian — On the Trinity | ANF 5: 노바티아누스 — 삼위일체론 | Novatian | ~258 | 10 | CCEL |
| 507 | anf-vol6-gregory-thaumaturgus | ANF Vol.6: Gregory Thaumaturgus | ANF 6: 기적의 그레고리 | Gregory Thaumaturgus | ~270 | 10 | CCEL |
| 508 | anf-vol6-dionysius-alex | ANF Vol.6: Dionysius of Alexandria | ANF 6: 알렉산드리아의 디오니시우스 | Dionysius | ~264 | 8 | CCEL |
| 509 | anf-vol6-methodius | ANF Vol.6: Methodius — Banquet of Ten Virgins | ANF 6: 메토디우스 — 열 처녀의 연회 | Methodius | ~311 | 12 | CCEL |
| 510 | anf-vol6-arnobius | ANF Vol.6: Arnobius Against the Heathen | ANF 6: 아르노비우스 — 이교 반박 | Arnobius | ~330 | 12 | CCEL |
| 511 | anf-vol7-lactantius | ANF Vol.7: Lactantius — Divine Institutes | ANF 7: 락탄티우스 — 신적 교훈 | Lactantius | ~325 | 15 | CCEL |
| 512 | anf-vol7-venantius | ANF Vol.7: Venantius — Poems | ANF 7: 베난티우스 — 시 | Venantius | ~600 | 8 | CCEL |
| 513 | anf-vol7-apostolic-constitutions | ANF Vol.7: Apostolic Constitutions (sel.) | ANF 7: 사도 규범 (선집) | Anonymous | ~380 | 15 | CCEL |
| 514 | anf-vol8-pseudo-clementine | ANF Vol.8: Pseudo-Clementine Recognitions | ANF 8: 위(僞)클레멘트 인지록 | Pseudo-Clement | ~320 | 15 | CCEL |
| 515 | anf-vol9-syriac-documents | ANF Vol.9: Syriac Documents (selections) | ANF 9: 시리아어 문서 (선집) | Various | 3~5C | 12 | CCEL |

### 20B. NPNF 1st Series 확장

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 516 | npnf1-vol1-augustine-confessions-full | NPNF1 Vol.1: Confessions (annotated) | 고백록 (주석판) | Augustine | 430 | 15 | CCEL |
| 517 | npnf1-vol1-augustine-letters-sel | NPNF1 Vol.1: Letters (selections) | 서신 선집 | Augustine | 430 | 15 | CCEL |
| 518 | npnf1-vol2-city-of-god-v2 | NPNF1 Vol.2: City of God (expansion) | 신국론 (확장) | Augustine | 430 | 20 | CCEL |
| 519 | npnf1-vol4-augustine-anti-donatist | NPNF1 Vol.4: Anti-Donatist Writings | 반(反)도나투스파 저작 | Augustine | 430 | 15 | CCEL |
| 520 | npnf1-vol5-augustine-anti-pelagian | NPNF1 Vol.5: Anti-Pelagian Writings | 반(反)펠라기우스파 저작 | Augustine | 430 | 15 | CCEL |
| 521 | npnf1-vol6-augustine-sermon-mount | NPNF1 Vol.6: Sermon on the Mount / Harmony | 산상수훈 해설 / 복음서 조화 | Augustine | 430 | 15 | CCEL |
| 522 | npnf1-vol7-augustine-homilies-john | NPNF1 Vol.7: Homilies on John (selections) | 요한복음 강해 (선집) | Augustine | 430 | 20 | CCEL |
| 523 | npnf1-vol8-augustine-psalms-sel | NPNF1 Vol.8: Expositions on the Psalms (sel.) | 시편 강해 (선집) | Augustine | 430 | 20 | CCEL |
| 524 | npnf1-vol10-chrysostom-matthew-v2 | NPNF1 Vol.10: Homilies on Matthew (expansion) | 마태복음 강해 (확장) | John Chrysostom | 407 | 20 | CCEL |
| 525 | npnf1-vol11-chrysostom-acts-rom | NPNF1 Vol.11: Homilies on Acts and Romans | 사도행전/로마서 강해 | John Chrysostom | 407 | 20 | CCEL |
| 526 | npnf1-vol12-chrysostom-corinthians | NPNF1 Vol.12: Homilies on Corinthians | 고린도서 강해 | John Chrysostom | 407 | 20 | CCEL |
| 527 | npnf1-vol13-chrysostom-galatians | NPNF1 Vol.13: Homilies on Galatians-Philemon | 갈라디아서~빌레몬서 강해 | John Chrysostom | 407 | 20 | CCEL |
| 528 | npnf1-vol14-chrysostom-hebrews | NPNF1 Vol.14: Homilies on Hebrews | 히브리서 강해 | John Chrysostom | 407 | 15 | CCEL |

### 20C. NPNF 2nd Series 확장

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 529 | npnf2-vol1-eusebius-extra | NPNF2 Vol.1: Eusebius Supplementary | 에우세비우스 보충 저작 | Eusebius | 339 | 15 | CCEL |
| 530 | npnf2-vol2-socrates-sozomen-extra | NPNF2 Vol.2: Socrates/Sozomen Supplementary | 소크라테스/소조멘 보충 | Socrates/Sozomen | 5C | 15 | CCEL |
| 531 | npnf2-vol3-theodoret-extra | NPNF2 Vol.3: Theodoret Supplementary | 테오도렛 보충 저작 | Theodoret | 457 | 12 | CCEL |
| 532 | npnf2-vol4-athanasius-extra | NPNF2 Vol.4: Athanasius — Orations Against Arians | 아리우스파 반박 강론 | Athanasius | 373 | 15 | CCEL |
| 533 | npnf2-vol5-gregory-nyssa-extra2 | NPNF2 Vol.5: Gregory of Nyssa — Supplementary | 닛사의 그레고리 보충 | Gregory of Nyssa | 394 | 12 | CCEL |
| 534 | npnf2-vol6-jerome-extra | NPNF2 Vol.6: Jerome — Works & Letters | 제롬 — 저작과 서신 | Jerome | 420 | 15 | CCEL |
| 535 | npnf2-vol7-cyril-gregory-extra | NPNF2 Vol.7: Cyril/Gregory Naz. Supplementary | 키릴/나지안주스 보충 | Cyril/Gregory | 4C | 12 | CCEL |
| 536 | npnf2-vol8-basil-extra2 | NPNF2 Vol.8: Basil — Supplementary | 바실 보충 저작 | Basil the Great | 379 | 12 | CCEL |
| 537 | npnf2-vol9-hilary-poitiers | NPNF2 Vol.9: Hilary of Poitiers — On the Trinity | 힐라리 — 삼위일체론 | Hilary of Poitiers | 367 | 15 | CCEL |
| 538 | npnf2-vol9-john-damascene-extra | NPNF2 Vol.9: John of Damascus Supplementary | 다마스쿠스의 요한 보충 | John of Damascus | 749 | 10 | CCEL |
| 539 | npnf2-vol10-ambrose-extra | NPNF2 Vol.10: Ambrose Supplementary | 암브로시우스 보충 저작 | Ambrose | 397 | 12 | CCEL |
| 540 | npnf2-vol11-sulpicius-cassian-extra | NPNF2 Vol.11: Sulpicius/Cassian Supplementary | 술피키우스/카시안 보충 | Various | 5C | 12 | CCEL |
| 541 | npnf2-vol12-leo-gregory-great-extra | NPNF2 Vol.12: Leo/Gregory Great Supplementary | 레오/그레고리 대교황 보충 | Various | 6C | 12 | CCEL |
| 542 | npnf2-vol13-ephraim-aphrahat | NPNF2 Vol.13: Ephraim & Aphrahat | 에프라임과 아프라하트 | Various | 4C | 15 | CCEL |
| 543 | npnf2-vol14-seven-ecumenical | NPNF2 Vol.14: Seven Ecumenical Councils | 일곱 에큐메니컬 공의회 | Various | 4~8C | 20 | CCEL |
| 544 | npnf2-vol14-excursus | NPNF2 Vol.14: Excursus (selections) | 부록 해설 (선집) | Various | — | 12 | CCEL |
| 545 | augustine-de-trinitate-full | On the Trinity (complete) | 삼위일체론 (전체) | Augustine | 430 | 20 | CCEL |
| 546 | augustine-retractions | Retractions | 재고록 | Augustine | 430 | 10 | CCEL |
| 547 | augustine-soliloquies | Soliloquies | 독백록 | Augustine | 430 | 8 | CCEL / Gutenberg |
| 548 | augustine-free-will | On Free Will (De Libero Arbitrio) | 자유의지론 | Augustine | 430 | 10 | CCEL |
| 549 | augustine-catechizing-uninstructed | On the Catechising of the Uninstructed | 무지한 자의 교육 | Augustine | 430 | 8 | CCEL |
| 550 | augustine-continence | On Continence | 절제론 | Augustine | 430 | 8 | CCEL |
| 551 | chrysostom-genesis-homilies-sel | Homilies on Genesis (selections) | 창세기 강해 (선집) | John Chrysostom | 407 | 20 | CCEL |
| 552 | chrysostom-john-homilies-sel | Homilies on John (selections) | 요한복음 강해 (선집) | John Chrysostom | 407 | 20 | CCEL |
| 553 | chrysostom-ephesians-homilies | Homilies on Ephesians | 에베소서 강해 | John Chrysostom | 407 | 15 | CCEL |
| 554 | chrysostom-philippians-homilies | Homilies on Philippians | 빌립보서 강해 | John Chrysostom | 407 | 12 | CCEL |
| 555 | chrysostom-timothy-titus | Homilies on Timothy, Titus, Philemon | 디모데/디도/빌레몬 강해 | John Chrysostom | 407 | 15 | CCEL |

**소계**: 60권, ~850챕터, 예상 비용 ~$180

---

## 카테고리 21: 스펄전 확장 — 40권

> 설교의 왕자 C.H. Spurgeon (1834-1892)의 방대한 저작 확장

### 21A. Metropolitan Tabernacle Pulpit 추가

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 556 | spurgeon-sermons-v4 | MTP Vol.4 (Sermons 175-233) | 메트로폴리탄 설교집 제4권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 557 | spurgeon-sermons-v5 | MTP Vol.5 (Sermons 234-291) | 메트로폴리탄 설교집 제5권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 558 | spurgeon-sermons-v6 | MTP Vol.6 (Sermons 292-349) | 메트로폴리탄 설교집 제6권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 559 | spurgeon-sermons-v7 | MTP Vol.7 (Sermons 350-408) | 메트로폴리탄 설교집 제7권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 560 | spurgeon-sermons-v8 | MTP Vol.8 (Sermons 409-467) | 메트로폴리탄 설교집 제8권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 561 | spurgeon-sermons-v9 | MTP Vol.9 (Sermons 468-526) | 메트로폴리탄 설교집 제9권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 562 | spurgeon-sermons-v10 | MTP Vol.10 (Sermons 527-585) | 메트로폴리탄 설교집 제10권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 563 | spurgeon-sermons-v11 | MTP Vol.11 (Sermons 586-644) | 메트로폴리탄 설교집 제11권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 564 | spurgeon-sermons-v12 | MTP Vol.12 (Sermons 645-703) | 메트로폴리탄 설교집 제12권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 565 | spurgeon-sermons-v13 | MTP Vol.13 (Sermons 704-762) | 메트로폴리탄 설교집 제13권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 566 | spurgeon-sermons-v14 | MTP Vol.14 (Sermons 763-821) | 메트로폴리탄 설교집 제14권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 567 | spurgeon-sermons-v15 | MTP Vol.15 (Sermons 822-880) | 메트로폴리탄 설교집 제15권 | C.H. Spurgeon | 1892 | 20 | Archive |

### 21B. New Park Street Pulpit

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 568 | spurgeon-new-park-v1 | New Park Street Pulpit Vol.1 (1855) | 뉴파크 스트리트 설교 제1권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 569 | spurgeon-new-park-v2 | New Park Street Pulpit Vol.2 (1856) | 뉴파크 스트리트 설교 제2권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 570 | spurgeon-new-park-v3 | New Park Street Pulpit Vol.3 (1857) | 뉴파크 스트리트 설교 제3권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 571 | spurgeon-new-park-v4 | New Park Street Pulpit Vol.4 (1858) | 뉴파크 스트리트 설교 제4권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 572 | spurgeon-new-park-v5 | New Park Street Pulpit Vol.5 (1859) | 뉴파크 스트리트 설교 제5권 | C.H. Spurgeon | 1892 | 20 | Archive |
| 573 | spurgeon-new-park-v6 | New Park Street Pulpit Vol.6 (1860) | 뉴파크 스트리트 설교 제6권 | C.H. Spurgeon | 1892 | 20 | Archive |

### 21C. Treasury of David 확장 & 기타

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 574 | spurgeon-treasury-david-v2 | Treasury of David Vol.2 (Psalms 27-52) | 시편 강해 보물 제2권 | C.H. Spurgeon | 1892 | 20 | CCEL |
| 575 | spurgeon-treasury-david-v3 | Treasury of David Vol.3 (Psalms 53-78) | 시편 강해 보물 제3권 | C.H. Spurgeon | 1892 | 20 | CCEL |
| 576 | spurgeon-treasury-david-v4 | Treasury of David Vol.4 (Psalms 79-103) | 시편 강해 보물 제4권 | C.H. Spurgeon | 1892 | 20 | CCEL |
| 577 | spurgeon-treasury-david-v5 | Treasury of David Vol.5 (Psalms 104-118) | 시편 강해 보물 제5권 | C.H. Spurgeon | 1892 | 20 | CCEL |
| 578 | spurgeon-treasury-david-v6 | Treasury of David Vol.6 (Psalms 119-124) | 시편 강해 보물 제6권 | C.H. Spurgeon | 1892 | 20 | CCEL |
| 579 | spurgeon-treasury-david-v7 | Treasury of David Vol.7 (Psalms 125-150) | 시편 강해 보물 제7권 | C.H. Spurgeon | 1892 | 20 | CCEL |
| 580 | spurgeon-feathers-arrows | Feathers for Arrows | 화살을 위한 깃털 | C.H. Spurgeon | 1892 | 15 | Gutenberg |
| 581 | spurgeon-flowers-garden | Flowers from a Puritan's Garden | 청교도의 정원에서 온 꽃 | C.H. Spurgeon | 1892 | 15 | Archive |
| 582 | spurgeon-autobiography-v1 | Autobiography Vol.1: Early Years | 자서전 제1권: 초기 시절 | C.H. Spurgeon | 1892 | 20 | Archive |
| 583 | spurgeon-autobiography-v2 | Autobiography Vol.2: Full Harvest | 자서전 제2권: 풍성한 수확 | C.H. Spurgeon | 1892 | 20 | Archive |
| 584 | spurgeon-according-to-promise | According to Promise | 약속대로 | C.H. Spurgeon | 1892 | 10 | Gutenberg |
| 585 | spurgeon-come-ye-children | Come Ye Children | 아이들아 오너라 | C.H. Spurgeon | 1892 | 10 | Gutenberg |
| 586 | spurgeon-farm-sermons | Farm Sermons | 농장 설교 | C.H. Spurgeon | 1892 | 12 | Gutenberg |
| 587 | spurgeon-types-and-emblems | Types and Emblems | 예표와 상징 | C.H. Spurgeon | 1892 | 12 | Archive |
| 588 | spurgeon-sword-and-trowel-sel | Sword and Trowel (selections) | 검과 흙손 (선집) | C.H. Spurgeon | 1892 | 15 | Archive |
| 589 | spurgeon-words-of-wisdom | Words of Wisdom for Daily Life | 일상의 지혜 | C.H. Spurgeon | 1892 | 12 | Archive |
| 590 | spurgeon-christs-words-cross | Christ's Words from the Cross | 십자가 위의 말씀 | C.H. Spurgeon | 1892 | 8 | Gutenberg |
| 591 | spurgeon-twelve-sermons-holy-spirit | Twelve Sermons on the Holy Spirit | 성령에 관한 열두 설교 | C.H. Spurgeon | 1892 | 12 | Gutenberg |
| 592 | spurgeon-twelve-striking-sermons | Twelve Striking Sermons | 감동적인 열두 설교 | C.H. Spurgeon | 1892 | 12 | Gutenberg |
| 593 | spurgeon-devotional-classics | Spurgeon's Devotional Classics | 스펄전 묵상 고전 | C.H. Spurgeon | 1892 | 15 | Archive |
| 594 | spurgeon-gleanings-sermons | Gleanings Among the Sheaves | 곡식단 사이의 이삭줍기 | C.H. Spurgeon | 1892 | 10 | Gutenberg |
| 595 | spurgeon-metropolitan-tabernacle | The Metropolitan Tabernacle: Its History | 메트로폴리탄 성막: 역사 | C.H. Spurgeon | 1892 | 10 | Archive |

**소계**: 40권, ~690챕터, 예상 비용 ~$120

---

## 카테고리 22: 성경 주석 확장 — 80권

> 퍼블릭 도메인 성경 주석 시리즈 확장

### 22A. Jamieson-Fausset-Brown Commentary

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 596 | jfb-genesis | JFB Commentary: Genesis | JFB 주석: 창세기 | Jamieson, Fausset, Brown | 1910 | 15 | CCEL / Archive |
| 597 | jfb-exodus | JFB Commentary: Exodus | JFB 주석: 출애굽기 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 598 | jfb-leviticus-numbers | JFB Commentary: Leviticus-Numbers | JFB 주석: 레위기~민수기 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 599 | jfb-deuteronomy-joshua | JFB Commentary: Deuteronomy-Joshua | JFB 주석: 신명기~여호수아 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 600 | jfb-judges-ruth-samuel | JFB Commentary: Judges-1&2 Samuel | JFB 주석: 사사기~사무엘 | Jamieson, Fausset, Brown | 1910 | 15 | CCEL / Archive |
| 601 | jfb-kings-chronicles | JFB Commentary: 1&2 Kings, 1&2 Chronicles | JFB 주석: 열왕기~역대기 | Jamieson, Fausset, Brown | 1910 | 15 | CCEL / Archive |
| 602 | jfb-ezra-esther | JFB Commentary: Ezra-Esther | JFB 주석: 에스라~에스더 | Jamieson, Fausset, Brown | 1910 | 10 | CCEL / Archive |
| 603 | jfb-job | JFB Commentary: Job | JFB 주석: 욥기 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 604 | jfb-psalms | JFB Commentary: Psalms | JFB 주석: 시편 | Jamieson, Fausset, Brown | 1910 | 20 | CCEL / Archive |
| 605 | jfb-proverbs-ecclesiastes | JFB Commentary: Proverbs-Ecclesiastes-Song | JFB 주석: 잠언~아가 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 606 | jfb-isaiah | JFB Commentary: Isaiah | JFB 주석: 이사야 | Jamieson, Fausset, Brown | 1910 | 15 | CCEL / Archive |
| 607 | jfb-jeremiah-lamentations | JFB Commentary: Jeremiah-Lamentations | JFB 주석: 예레미야~애가 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 608 | jfb-ezekiel-daniel | JFB Commentary: Ezekiel-Daniel | JFB 주석: 에스겔~다니엘 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 609 | jfb-minor-prophets | JFB Commentary: Minor Prophets | JFB 주석: 소선지서 | Jamieson, Fausset, Brown | 1910 | 15 | CCEL / Archive |
| 610 | jfb-matthew | JFB Commentary: Matthew | JFB 주석: 마태복음 | Jamieson, Fausset, Brown | 1910 | 15 | CCEL / Archive |
| 611 | jfb-mark-luke | JFB Commentary: Mark-Luke | JFB 주석: 마가~누가복음 | Jamieson, Fausset, Brown | 1910 | 15 | CCEL / Archive |
| 612 | jfb-john | JFB Commentary: John | JFB 주석: 요한복음 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 613 | jfb-acts | JFB Commentary: Acts | JFB 주석: 사도행전 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 614 | jfb-romans | JFB Commentary: Romans | JFB 주석: 로마서 | Jamieson, Fausset, Brown | 1910 | 10 | CCEL / Archive |
| 615 | jfb-corinthians | JFB Commentary: 1&2 Corinthians | JFB 주석: 고린도전후서 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 616 | jfb-galatians-philemon | JFB Commentary: Galatians-Philemon | JFB 주석: 갈라디아서~빌레몬서 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |
| 617 | jfb-hebrews-revelation | JFB Commentary: Hebrews-Revelation | JFB 주석: 히브리서~계시록 | Jamieson, Fausset, Brown | 1910 | 12 | CCEL / Archive |

### 22B. Keil & Delitzsch OT Commentary

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 618 | kd-genesis | K&D OT Commentary: Genesis | K&D 구약주석: 창세기 | Keil & Delitzsch | 1890 | 15 | Archive |
| 619 | kd-exodus-leviticus | K&D OT Commentary: Exodus-Leviticus | K&D 구약주석: 출애굽기~레위기 | Keil & Delitzsch | 1890 | 15 | Archive |
| 620 | kd-numbers-deuteronomy | K&D OT Commentary: Numbers-Deuteronomy | K&D 구약주석: 민수기~신명기 | Keil & Delitzsch | 1890 | 15 | Archive |
| 621 | kd-joshua-judges-ruth | K&D OT Commentary: Joshua-Ruth | K&D 구약주석: 여호수아~룻기 | Keil & Delitzsch | 1890 | 12 | Archive |
| 622 | kd-samuel | K&D OT Commentary: 1&2 Samuel | K&D 구약주석: 사무엘상하 | Keil & Delitzsch | 1890 | 15 | Archive |
| 623 | kd-kings | K&D OT Commentary: 1&2 Kings | K&D 구약주석: 열왕기상하 | Keil & Delitzsch | 1890 | 15 | Archive |
| 624 | kd-chronicles-ezra-nehemiah | K&D OT Commentary: Chronicles-Nehemiah | K&D 구약주석: 역대기~느헤미야 | Keil & Delitzsch | 1890 | 15 | Archive |
| 625 | kd-esther-job | K&D OT Commentary: Esther-Job | K&D 구약주석: 에스더~욥기 | Keil & Delitzsch | 1890 | 12 | Archive |
| 626 | kd-psalms | K&D OT Commentary: Psalms | K&D 구약주석: 시편 | Keil & Delitzsch | 1890 | 20 | Archive |
| 627 | kd-proverbs-song | K&D OT Commentary: Proverbs-Song | K&D 구약주석: 잠언~아가 | Keil & Delitzsch | 1890 | 12 | Archive |
| 628 | kd-isaiah | K&D OT Commentary: Isaiah | K&D 구약주석: 이사야 | Keil & Delitzsch | 1890 | 15 | Archive |
| 629 | kd-jeremiah-lamentations | K&D OT Commentary: Jeremiah-Lamentations | K&D 구약주석: 예레미야~애가 | Keil & Delitzsch | 1890 | 12 | Archive |
| 630 | kd-ezekiel-daniel | K&D OT Commentary: Ezekiel-Daniel | K&D 구약주석: 에스겔~다니엘 | Keil & Delitzsch | 1890 | 12 | Archive |
| 631 | kd-minor-prophets | K&D OT Commentary: Minor Prophets | K&D 구약주석: 소선지서 | Keil & Delitzsch | 1890 | 15 | Archive |

### 22C. Ellicott's Commentary & 기타

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 632 | ellicott-matthew | Ellicott's Commentary: Matthew | 엘리콧 주석: 마태복음 | Charles J. Ellicott | 1905 | 15 | Archive |
| 633 | ellicott-mark-luke | Ellicott's Commentary: Mark-Luke | 엘리콧 주석: 마가~누가복음 | Charles J. Ellicott | 1905 | 15 | Archive |
| 634 | ellicott-john-acts | Ellicott's Commentary: John-Acts | 엘리콧 주석: 요한복음~사도행전 | Charles J. Ellicott | 1905 | 15 | Archive |
| 635 | ellicott-romans-corinthians | Ellicott's Commentary: Romans-2 Corinthians | 엘리콧 주석: 로마서~고린도후서 | Charles J. Ellicott | 1905 | 15 | Archive |
| 636 | ellicott-galatians-thessalonians | Ellicott's Commentary: Galatians-2 Thessalonians | 엘리콧 주석: 갈라디아~데살로니가 | Charles J. Ellicott | 1905 | 12 | Archive |
| 637 | ellicott-timothy-revelation | Ellicott's Commentary: 1 Timothy-Revelation | 엘리콧 주석: 디모데전~계시록 | Charles J. Ellicott | 1905 | 15 | Archive |
| 638 | expositors-bible-genesis | Expositor's Bible: Genesis | 설교자의 성경: 창세기 | Marcus Dods | 1909 | 15 | Archive / CCEL |
| 639 | expositors-bible-exodus | Expositor's Bible: Exodus | 설교자의 성경: 출애굽기 | G. Rawlinson | 1902 | 12 | Archive |
| 640 | expositors-bible-psalms | Expositor's Bible: Psalms (selections) | 설교자의 성경: 시편 (선집) | Alexander Maclaren | 1910 | 20 | Archive / CCEL |
| 641 | expositors-bible-isaiah | Expositor's Bible: Isaiah (selections) | 설교자의 성경: 이사야 (선집) | George Adam Smith | 1942 | 15 | Archive |
| 642 | expositors-bible-john | Expositor's Bible: Gospel of John | 설교자의 성경: 요한복음 | Marcus Dods | 1909 | 15 | Archive / CCEL |
| 643 | expositors-bible-acts | Expositor's Bible: Acts | 설교자의 성경: 사도행전 | G.T. Stokes | 1898 | 12 | Archive |
| 644 | expositors-bible-romans | Expositor's Bible: Romans | 설교자의 성경: 로마서 | Handley C.G. Moule | 1920 | 12 | Archive |
| 645 | expositors-bible-corinthians | Expositor's Bible: 1 Corinthians | 설교자의 성경: 고린도전서 | Marcus Dods | 1909 | 12 | Archive |
| 646 | expositors-bible-ephesians | Expositor's Bible: Ephesians | 설교자의 성경: 에베소서 | G.G. Findlay | 1919 | 10 | Archive |
| 647 | expositors-bible-hebrews | Expositor's Bible: Hebrews | 설교자의 성경: 히브리서 | T.C. Edwards | 1900 | 12 | Archive |
| 648 | expositors-bible-revelation | Expositor's Bible: Revelation | 설교자의 성경: 요한계시록 | W. Milligan | 1893 | 12 | Archive |
| 649 | calvin-commentary-genesis | Calvin's Commentary: Genesis | 칼빈 주석: 창세기 | John Calvin | 1564 | 20 | CCEL |
| 650 | calvin-commentary-exodus-deut | Calvin's Commentary: Exodus-Deuteronomy (sel.) | 칼빈 주석: 출애굽기~신명기 (선집) | John Calvin | 1564 | 20 | CCEL |
| 651 | calvin-commentary-joshua | Calvin's Commentary: Joshua | 칼빈 주석: 여호수아 | John Calvin | 1564 | 12 | CCEL |
| 652 | calvin-commentary-isaiah-sel | Calvin's Commentary: Isaiah (selections) | 칼빈 주석: 이사야 (선집) | John Calvin | 1564 | 20 | CCEL |
| 653 | calvin-commentary-jeremiah-sel | Calvin's Commentary: Jeremiah (selections) | 칼빈 주석: 예레미야 (선집) | John Calvin | 1564 | 15 | CCEL |
| 654 | calvin-commentary-minor-prophets | Calvin's Commentary: Minor Prophets (sel.) | 칼빈 주석: 소선지서 (선집) | John Calvin | 1564 | 15 | CCEL |
| 655 | calvin-commentary-john | Calvin's Commentary: John | 칼빈 주석: 요한복음 | John Calvin | 1564 | 15 | CCEL |
| 656 | calvin-commentary-acts-sel | Calvin's Commentary: Acts (selections) | 칼빈 주석: 사도행전 (선집) | John Calvin | 1564 | 15 | CCEL |
| 657 | calvin-commentary-corinthians | Calvin's Commentary: 1&2 Corinthians | 칼빈 주석: 고린도전후서 | John Calvin | 1564 | 15 | CCEL |
| 658 | calvin-commentary-galatians-eph | Calvin's Commentary: Galatians-Ephesians | 칼빈 주석: 갈라디아서~에베소서 | John Calvin | 1564 | 12 | CCEL |
| 659 | calvin-commentary-philippians-col | Calvin's Commentary: Philippians-Colossians | 칼빈 주석: 빌립보서~골로새서 | John Calvin | 1564 | 10 | CCEL |
| 660 | calvin-commentary-timothy-titus | Calvin's Commentary: Timothy-Titus-Philemon | 칼빈 주석: 디모데~빌레몬 | John Calvin | 1564 | 10 | CCEL |
| 661 | calvin-commentary-hebrews | Calvin's Commentary: Hebrews | 칼빈 주석: 히브리서 | John Calvin | 1564 | 12 | CCEL |
| 662 | luther-commentary-galatians-full | Luther's Commentary: Galatians (full) | 루터 주석: 갈라디아서 (전체) | Martin Luther | 1546 | 15 | CCEL / Gutenberg |
| 663 | luther-commentary-romans-sel | Luther's Lectures on Romans (selections) | 루터의 로마서 강의 (선집) | Martin Luther | 1546 | 15 | Archive |
| 664 | poole-annotations-sel-v1 | Poole's Annotations: OT Selections Vol.1 | 풀 주석: 구약 선집 제1권 | Matthew Poole | 1679 | 20 | Archive |
| 665 | poole-annotations-sel-v2 | Poole's Annotations: OT Selections Vol.2 | 풀 주석: 구약 선집 제2권 | Matthew Poole | 1679 | 20 | Archive |
| 666 | poole-annotations-sel-nt | Poole's Annotations: NT Selections | 풀 주석: 신약 선집 | Matthew Poole | 1679 | 20 | Archive |
| 667 | gill-commentary-genesis | Gill's Commentary: Genesis | 길 주석: 창세기 | John Gill | 1771 | 15 | CCEL / Archive |
| 668 | gill-commentary-psalms-sel | Gill's Commentary: Psalms (selections) | 길 주석: 시편 (선집) | John Gill | 1771 | 20 | CCEL / Archive |
| 669 | gill-commentary-isaiah-sel | Gill's Commentary: Isaiah (selections) | 길 주석: 이사야 (선집) | John Gill | 1771 | 15 | CCEL / Archive |
| 670 | gill-commentary-matthew | Gill's Commentary: Matthew | 길 주석: 마태복음 | John Gill | 1771 | 15 | CCEL / Archive |
| 671 | gill-commentary-john | Gill's Commentary: John | 길 주석: 요한복음 | John Gill | 1771 | 12 | CCEL / Archive |
| 672 | gill-commentary-acts | Gill's Commentary: Acts | 길 주석: 사도행전 | John Gill | 1771 | 12 | CCEL / Archive |
| 673 | gill-commentary-hebrews | Gill's Commentary: Hebrews | 길 주석: 히브리서 | John Gill | 1771 | 10 | CCEL / Archive |
| 674 | gill-commentary-revelation | Gill's Commentary: Revelation | 길 주석: 요한계시록 | John Gill | 1771 | 12 | CCEL / Archive |
| 675 | clarke-commentary-sel-v1 | Adam Clarke's Commentary: Pentateuch (sel.) | 아담 클라크 주석: 모세오경 (선집) | Adam Clarke | 1832 | 15 | Archive |

**소계**: 80권, ~1,115챕터, 예상 비용 ~$240

---

## 카테고리 23: 추가 설교 모음집 — 40권

> 19세기~20세기 초 주요 설교자 확장

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 676 | morgan-gospel-matthew | The Gospel According to Matthew | 마태복음 강해 | G. Campbell Morgan | 1945 | 15 | Archive |
| 677 | morgan-gospel-mark | The Gospel According to Mark | 마가복음 강해 | G. Campbell Morgan | 1945 | 12 | Archive |
| 678 | morgan-gospel-luke | The Gospel According to Luke | 누가복음 강해 | G. Campbell Morgan | 1945 | 15 | Archive |
| 679 | morgan-gospel-john | The Gospel According to John | 요한복음 강해 | G. Campbell Morgan | 1945 | 15 | Archive |
| 680 | morgan-acts-of-apostles | The Acts of the Apostles | 사도행전 강해 | G. Campbell Morgan | 1945 | 15 | Archive |
| 681 | morgan-westminster-pulpit-v1 | The Westminster Pulpit Vol.1 | 웨스트민스터 설교 제1권 | G. Campbell Morgan | 1945 | 20 | Archive |
| 682 | morgan-westminster-pulpit-v2 | The Westminster Pulpit Vol.2 | 웨스트민스터 설교 제2권 | G. Campbell Morgan | 1945 | 20 | Archive |
| 683 | morgan-ten-commandments | The Ten Commandments | 십계명 | G. Campbell Morgan | 1945 | 12 | Archive |
| 684 | parker-peoples-bible-sel-v2 | The People's Bible Vol.2 (selections) | 민중의 성경 제2권 (선집) | Joseph Parker | 1902 | 20 | Archive |
| 685 | parker-inner-life-of-christ-v1 | The Inner Life of Christ Vol.1 | 그리스도의 내적 삶 제1권 | Joseph Parker | 1902 | 15 | Archive |
| 686 | parker-inner-life-of-christ-v2 | The Inner Life of Christ Vol.2 | 그리스도의 내적 삶 제2권 | Joseph Parker | 1902 | 15 | Archive |
| 687 | parker-inner-life-of-christ-v3 | The Inner Life of Christ Vol.3 | 그리스도의 내적 삶 제3권 | Joseph Parker | 1902 | 15 | Archive |
| 688 | pierson-many-infallible-proofs | Many Infallible Proofs | 수많은 확실한 증거들 | Arthur T. Pierson | 1911 | 12 | Archive |
| 689 | pierson-new-acts-apostles | The New Acts of the Apostles | 새로운 사도행전 | Arthur T. Pierson | 1911 | 15 | Archive |
| 690 | simpson-gospel-john | The Gospel According to John | 요한복음 강해 | A.B. Simpson | 1919 | 15 | Archive |
| 691 | simpson-christ-in-bible-sel | Christ in the Bible (selections) | 성경 속의 그리스도 (선집) | A.B. Simpson | 1919 | 20 | Archive |
| 692 | simpson-larger-christian-life | The Self-Life and the Christ-Life | 자아적 삶과 그리스도적 삶 | A.B. Simpson | 1919 | 12 | Archive |
| 693 | chadwick-gospel-mark | The Gospel of Mark (Expositor's Bible) | 마가복음 강해 | G.A. Chadwick | 1914 | 12 | Archive |
| 694 | dods-first-corinthians | Expositor's Bible: 1 Corinthians | 고린도전서 강해 | Marcus Dods | 1909 | 12 | Archive |
| 695 | dale-ephesians | Lectures on Ephesians | 에베소서 강의 | R.W. Dale | 1895 | 12 | Archive |
| 696 | liddon-divinity-lord | The Divinity of Our Lord | 우리 주의 신성 | H.P. Liddon | 1890 | 12 | Archive |
| 697 | maclaren-colossians-philemon | Colossians and Philemon | 골로새서와 빌레몬 | Alexander Maclaren | 1910 | 10 | Archive |
| 698 | moule-philippian-studies | Philippian Studies | 빌립보서 연구 | Handley C.G. Moule | 1920 | 10 | Archive |
| 699 | moule-ephesian-studies | Ephesian Studies | 에베소서 연구 | Handley C.G. Moule | 1920 | 10 | Archive |
| 700 | moule-colossian-studies | Colossian Studies | 골로새서 연구 | Handley C.G. Moule | 1920 | 10 | Archive |
| 701 | whyte-appreciation-literature | An Appreciation of Literature | 문학 감상 | Alexander Whyte | 1921 | 10 | Archive |
| 702 | whyte-lord-teach-us-pray | Lord, Teach Us to Pray | 주여, 기도를 가르쳐 주소서 | Alexander Whyte | 1921 | 12 | Archive |
| 703 | jowett-high-calling | The High Calling | 높은 부르심 | John Henry Jowett | 1923 | 12 | Archive |
| 704 | jowett-brooks-by-way | Brooks by the Way | 길가의 시냇물 | John Henry Jowett | 1923 | 12 | Archive |
| 705 | jefferson-cardinal-ideas | Cardinal Ideas of Isaiah | 이사야의 핵심 사상 | Charles E. Jefferson | 1938 | 10 | Archive |
| 706 | jefferson-cardinal-ideas-jeremiah | Cardinal Ideas of Jeremiah | 예레미야의 핵심 사상 | Charles E. Jefferson | 1938 | 10 | Archive |
| 707 | stalker-life-jesus | The Life of Jesus Christ | 예수 그리스도의 생애 | James Stalker | 1927 | 12 | Gutenberg |
| 708 | stalker-life-paul | The Life of St. Paul | 사도 바울의 생애 | James Stalker | 1927 | 12 | Gutenberg |
| 709 | stalker-trial-jesus | The Trial and Death of Jesus Christ | 예수 그리스도의 재판과 죽음 | James Stalker | 1927 | 12 | Archive |
| 710 | mcintyre-hidden-life-prayer | The Hidden Life of Prayer | 기도의 숨겨진 삶 | David M. McIntyre | 1957 | 10 | Archive |
| 711 | gordon-ministry-spirit | The Ministry of the Spirit | 성령의 사역 | A.J. Gordon | 1895 | 12 | Archive / CCEL |
| 712 | gordon-twofold-life | The Twofold Life | 이중적 삶 | A.J. Gordon | 1895 | 10 | Archive |
| 713 | gordon-in-christ | In Christ | 그리스도 안에서 | A.J. Gordon | 1895 | 10 | Archive |
| 714 | talmage-sermons-v2 | Sermons of T. DeWitt Talmage Vol.2 | 탈마지 설교집 제2권 | T. DeWitt Talmage | 1902 | 20 | Archive |
| 715 | talmage-around-tea-table | Around the Tea-Table | 차 탁자 주위에서 | T. DeWitt Talmage | 1902 | 12 | Gutenberg |

**소계**: 40권, ~532챕터, 예상 비용 ~$120

---

## 카테고리 24: 19~20세기 초 경건 서적 확장 — 60권

> E.M. Bounds 기도 시리즈, S.D. Gordon 확장, 기타 경건 저작

### 24A. E.M. Bounds 기도 시리즈

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 716 | bounds-preacher-prayer | Preacher and Prayer | 설교자와 기도 | E.M. Bounds | 1913 | 10 | CCEL |
| 717 | bounds-purpose-prayer | The Purpose in Prayer | 기도의 목적 | E.M. Bounds | 1913 | 10 | CCEL |
| 718 | bounds-weapon-prayer | The Weapon of Prayer | 기도의 무기 | E.M. Bounds | 1913 | 10 | CCEL |
| 719 | bounds-necessity-prayer | The Necessity of Prayer | 기도의 필요성 | E.M. Bounds | 1913 | 10 | CCEL |
| 720 | bounds-possibilities-prayer | The Possibilities of Prayer | 기도의 가능성 | E.M. Bounds | 1913 | 10 | CCEL |
| 721 | bounds-reality-prayer | The Reality of Prayer | 기도의 실제 | E.M. Bounds | 1913 | 10 | CCEL |
| 722 | bounds-essentials-prayer | The Essentials of Prayer | 기도의 본질 | E.M. Bounds | 1913 | 10 | CCEL |

### 24B. S.D. Gordon "Quiet Talks" 시리즈

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 723 | gordon-quiet-talks-jesus | Quiet Talks About Jesus | 예수에 대한 조용한 대화 | S.D. Gordon | 1936 | 12 | Gutenberg |
| 724 | gordon-quiet-talks-service | Quiet Talks on Service | 봉사에 대한 조용한 대화 | S.D. Gordon | 1936 | 12 | Gutenberg |
| 725 | gordon-quiet-talks-home-ideals | Quiet Talks on Home Ideals | 가정의 이상에 대한 조용한 대화 | S.D. Gordon | 1936 | 10 | Gutenberg |
| 726 | gordon-quiet-talks-personal-problems | Quiet Talks on Personal Problems | 개인 문제에 대한 조용한 대화 | S.D. Gordon | 1936 | 10 | Gutenberg |
| 727 | gordon-quiet-talks-tempter | Quiet Talks About the Tempter | 시험자에 대한 조용한 대화 | S.D. Gordon | 1936 | 10 | Gutenberg |
| 728 | gordon-quiet-talks-simple-essentials | Quiet Talks on Simple Essentials | 단순한 본질에 대한 조용한 대화 | S.D. Gordon | 1936 | 10 | Gutenberg |

### 24C. Andrew Murray 추가

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 729 | murray-master-secret | The Master's Indwelling | 주인의 내주 | Andrew Murray | 1917 | 12 | CCEL |
| 730 | murray-inner-chamber | The Inner Chamber | 골방 | Andrew Murray | 1917 | 10 | CCEL |
| 731 | murray-like-christ | Like Christ | 그리스도를 닮아 | Andrew Murray | 1917 | 15 | CCEL |
| 732 | murray-full-blessing | The Full Blessing of Pentecost | 오순절의 충만한 축복 | Andrew Murray | 1917 | 12 | CCEL |
| 733 | murray-new-life | The New Life | 새 생명 | Andrew Murray | 1917 | 15 | CCEL |
| 734 | murray-state-of-church | The State of the Church | 교회의 상태 | Andrew Murray | 1917 | 10 | CCEL |
| 735 | murray-ministry-intercession | The Ministry of Intercession | 중보 기도의 사역 | Andrew Murray | 1917 | 12 | CCEL |
| 736 | murray-raising-dead | Raising Your Children for Christ | 자녀 양육 | Andrew Murray | 1917 | 12 | CCEL |

### 24D. 기타 경건 서적

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 737 | simpson-fullness-christ | The Fullness of Christ | 그리스도의 충만 | A.B. Simpson | 1919 | 12 | Archive |
| 738 | simpson-gospel-healing | The Gospel of Healing | 치유의 복음 | A.B. Simpson | 1919 | 12 | Archive |
| 739 | simpson-wholly-sanctified | Wholly Sanctified | 온전한 성화 | A.B. Simpson | 1919 | 10 | Archive |
| 740 | simpson-days-of-heaven | Days of Heaven Upon Earth | 땅 위의 천국 같은 날들 | A.B. Simpson | 1919 | 15 | Archive |
| 741 | trumbull-taking-men-alive | Taking Men Alive | 살아있는 영혼을 낚다 | Charles G. Trumbull | 1941 | 10 | Archive |
| 742 | trumbull-victory-life | The Life That Wins | 승리하는 삶 | Charles G. Trumbull | 1941 | 10 | Archive |
| 743 | pierson-acts-holy-spirit | The Acts of the Holy Spirit | 성령의 행적 | Arthur T. Pierson | 1911 | 12 | Archive |
| 744 | andrew-bonar-diary | Diary and Life of Andrew Bonar | 앤드류 보나르 일기와 삶 | Marjory Bonar (ed.) | 1892 | 15 | Archive |
| 745 | mccheyne-sermons-remains | Sermons and Remains | 설교와 유고 | R.M. M'Cheyne | 1843 | 15 | CCEL |
| 746 | torrey-divine-healing | Divine Healing | 신적 치유 | R.A. Torrey | 1928 | 8 | Archive |
| 747 | torrey-what-bible-teaches | What the Bible Teaches | 성경이 가르치는 것 | R.A. Torrey | 1928 | 15 | Archive |
| 748 | torrey-how-bring-men-christ | How to Bring Men to Christ | 사람들을 그리스도께 인도하는 법 | R.A. Torrey | 1928 | 10 | Archive / Gutenberg |
| 749 | torrey-how-to-obtain-fullness | How to Obtain Fullness of Power | 능력의 충만을 얻는 법 | R.A. Torrey | 1928 | 10 | Archive |
| 750 | havergal-morning-stars | Morning Stars | 새벽별 | Frances Ridley Havergal | 1879 | 10 | Archive |
| 751 | havergal-morning-bells | Morning Bells | 새벽 종소리 | Frances Ridley Havergal | 1879 | 10 | Archive |
| 752 | smith-every-day-religion | Every-Day Religion | 매일의 종교 | Hannah Whitall Smith | 1911 | 12 | Archive |
| 753 | carmichael-gold-cord | Gold Cord (selections) | 금줄 (선집) | Amy Carmichael | 1951 | 12 | Archive |
| 754 | carmichael-if | If | 만일 | Amy Carmichael | 1951 | 8 | Archive |
| 755 | carmichael-rose-from-brier | Rose from Brier | 가시에서 핀 장미 | Amy Carmichael | 1951 | 10 | Archive |
| 756 | huegel-bone-of-his-bone | Bone of His Bone | 그의 뼈 중의 뼈 | F.J. Huegel | 1971 | 8 | Archive |
| 757 | nee-sit-walk-stand | Sit, Walk, Stand | 앉으라, 걸으라, 서라 | Watchman Nee | 1972 | 8 | Archive |
| 758 | nee-release-of-spirit | The Release of the Spirit | 영의 해방 | Watchman Nee | 1972 | 10 | Archive |
| 759 | thomas-daily-readings | Daily Readings (selections) | 매일 묵상 (선집) | W.H. Griffith Thomas | 1924 | 15 | Archive |
| 760 | meyer-five-musts | Five Musts of the Christian Life | 기독교인의 다섯 가지 의무 | F.B. Meyer | 1929 | 8 | Archive |
| 761 | meyer-joshua-and-land-promise | Joshua and the Land of Promise | 여호수아와 약속의 땅 | F.B. Meyer | 1929 | 12 | Archive |
| 762 | meyer-david | David: Shepherd, Psalmist, King | 다윗: 목자, 시인, 왕 | F.B. Meyer | 1929 | 15 | Archive |
| 763 | meyer-paul | Paul: Servant of Jesus Christ | 바울: 예수 그리스도의 종 | F.B. Meyer | 1929 | 15 | Archive |
| 764 | meyer-abraham | Abraham, or the Obedience of Faith | 아브라함, 믿음의 순종 | F.B. Meyer | 1929 | 12 | Archive |
| 765 | meyer-peter | Peter: Fisherman, Disciple, Apostle | 베드로: 어부, 제자, 사도 | F.B. Meyer | 1929 | 12 | Archive |
| 766 | meyer-joseph | Joseph: Beloved, Hated, Exalted | 요셉: 사랑받고, 미움받고, 높임받다 | F.B. Meyer | 1929 | 12 | Archive |
| 767 | pierson-bible-and-spiritual-life | The Bible and Spiritual Life | 성경과 영적 생활 | Arthur T. Pierson | 1911 | 12 | Archive |
| 768 | moody-way-to-god-expanded | The Way to God (expanded) | 하나님께 가는 길 (확장판) | D.L. Moody | 1899 | 12 | Gutenberg |
| 769 | moody-men-of-bible | Men of the Bible | 성경의 인물들 | D.L. Moody | 1899 | 12 | Gutenberg |
| 770 | moody-sowing-reaping | Sowing and Reaping | 심고 거두기 | D.L. Moody | 1899 | 10 | Gutenberg |
| 771 | moody-heaven | Heaven: Where It Is | 천국: 그곳은 어디인가 | D.L. Moody | 1899 | 10 | Gutenberg |
| 772 | moody-to-the-work | To the Work! To the Work! | 일하라! 일하라! | D.L. Moody | 1899 | 10 | Gutenberg |
| 773 | moody-twelve-select-sermons | Twelve Select Sermons | 열두 선별 설교 | D.L. Moody | 1899 | 12 | Gutenberg |
| 774 | moody-short-talks | Short Talks | 짧은 이야기들 | D.L. Moody | 1899 | 12 | Gutenberg |
| 775 | pentecost-in-burning-bush | In the Volume of the Book | 책의 권에서 | George F. Pentecost | 1920 | 10 | Archive |

**소계**: 60권, ~685챕터, 예상 비용 ~$180

---

## 카테고리 25: 추가 종교개혁 & 신앙고백 — 20권

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 776 | scots-confession | Scots Confession (1560) | 스코틀랜드 신앙고백 | John Knox et al. | 1572 | 8 | CCEL |
| 777 | savoy-declaration | Savoy Declaration (1658) | 사보이 선언 | Independents | 1658 | 10 | CCEL |
| 778 | london-baptist-confession | London Baptist Confession (1689) | 런던 침례교 신앙고백 | Particular Baptists | 1689 | 12 | CCEL |
| 779 | thirty-nine-articles | Thirty-Nine Articles of Religion | 39개 조항 | Church of England | 1571 | 8 | CCEL |
| 780 | irish-articles | Irish Articles of Religion (1615) | 아일랜드 신앙 조항 | James Ussher | 1656 | 8 | CCEL |
| 781 | formula-of-concord | Formula of Concord | 일치 신조 | Lutheran Theologians | 1577 | 12 | CCEL |
| 782 | athanasian-creed-commentary | Athanasian Creed with Commentary | 아타나시우스 신경 해설 | Various | — | 6 | CCEL |
| 783 | apostles-creed-commentary | The Apostles' Creed: Commentary | 사도신경 해설 | Various | — | 8 | Archive |
| 784 | nicene-creed-history | The Nicene Creed: History and Theology | 니케아 신경: 역사와 신학 | Various | — | 8 | Archive |
| 785 | ames-marrow-theology | The Marrow of Theology | 신학의 정수 | William Ames | 1633 | 15 | CCEL / Archive |
| 786 | turretin-institutes-sel | Institutes of Elenctic Theology (selections) | 논쟁 신학 강요 (선집) | Francis Turretin | 1687 | 20 | Archive |
| 787 | witsius-economy-covenants-sel | Economy of the Covenants (selections) | 언약의 경륜 (선집) | Herman Witsius | 1708 | 15 | Archive |
| 788 | ursinus-commentary-catechism | Commentary on the Heidelberg Catechism | 하이델베르크 교리문답 주석 | Zacharias Ursinus | 1583 | 15 | CCEL / Archive |
| 789 | vermigli-commonplaces-sel | Common Places (selections) | 신학 공동 논제 (선집) | Peter Martyr Vermigli | 1562 | 12 | Archive |
| 790 | bucer-true-pastoral-care | Concerning the True Care of Souls | 참된 영혼 돌봄에 관하여 | Martin Bucer | 1551 | 10 | Archive |
| 791 | bullinger-decades-sel | Decades (selections) | 십일론 (선집) | Heinrich Bullinger | 1575 | 15 | Archive |
| 792 | beza-confession | Confession of Faith | 신앙고백 | Theodore Beza | 1605 | 8 | CCEL / Archive |
| 793 | owen-biblical-theology-sel | Biblical Theology (selections) | 성경신학 (선집) | John Owen | 1683 | 12 | CCEL |
| 794 | goodwin-works-sel | Selected Works of Thomas Goodwin | 토마스 굿윈 선집 | Thomas Goodwin | 1680 | 15 | CCEL |
| 795 | rutherford-trial-triumph | The Trial and Triumph of Faith | 믿음의 시련과 승리 | Samuel Rutherford | 1661 | 12 | CCEL / Archive |

**소계**: 20권, ~229챕터, 예상 비용 ~$60

---

## 카테고리 26: 추가 선교사 전기 & 여성 신앙인 — 30권

### 26A. 추가 선교사 전기

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 796 | martyn-journals-sel | Journals and Letters (selections) | 일기와 서신 (선집) | Henry Martyn | 1812 | 15 | Archive |
| 797 | duff-alexander-life | Life of Alexander Duff | 알렉산더 더프의 생애 | George Smith | 1878 | 15 | Archive |
| 798 | hannington-bishop-last-journals | Last Journals of Bishop Hannington | 해닝턴 주교의 마지막 일기 | E.C. Dawson | 1885 | 12 | Archive |
| 799 | grenfell-labrador | A Labrador Doctor | 래브라도르의 의사 | Wilfred Grenfell | 1940 | 15 | Archive / Gutenberg |
| 800 | elliot-jim-story | Through Gates of Splendor (selections) | 영광의 문을 통과하여 (선집) | Elisabeth Elliot | 2015 | 12 | Archive |
| 801 | gilmour-among-mongols | Among the Mongols | 몽골인들 가운데서 | James Gilmour | 1891 | 15 | Gutenberg / Archive |
| 802 | coillard-on-threshold-africa | On the Threshold of Central Africa | 중앙 아프리카의 문턱에서 | François Coillard | 1904 | 15 | Archive |
| 803 | gardiner-allen-biography | Allen Gardiner: Pioneer Missionary | 앨런 가디너: 개척 선교사 | John W. Marsh | 1851 | 12 | Archive |
| 804 | stewart-lovedale-south-africa | Lovedale: South Africa | 러브데일: 남아프리카 | James Stewart | 1905 | 12 | Archive |
| 805 | scudder-nineteen-centuries | Nineteen Centuries of Missions | 19세기의 선교 | Doremus Scudder | 1931 | 12 | Archive |
| 806 | zwemer-islam-challenge | Islam: A Challenge to Faith | 이슬람: 신앙에 대한 도전 | Samuel Zwemer | 1952 | 12 | Archive |
| 807 | verbeck-guido-japan | Guido Verbeck of Japan | 일본의 기도 버벡 | William Elliot Griffis | 1928 | 15 | Archive |
| 808 | ross-john-korea | Mission to Korea | 한국 선교 | John Ross | 1915 | 12 | Archive |

### 26B. 추가 여성 신앙 저작

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 809 | booth-catherine-female-ministry | Female Ministry | 여성 사역 | Catherine Booth | 1890 | 10 | Archive |
| 810 | carmichael-kohila | Kohila | 코힐라 | Amy Carmichael | 1951 | 12 | Archive |
| 811 | guyon-spiritual-progress | Spiritual Progress | 영적 진보 | Madame Guyon | 1717 | 10 | CCEL |
| 812 | judson-ann-life | Life and Writings of Ann Judson | 앤 저드슨의 삶과 글 | James D. Knowles | 1826 | 15 | Archive / Gutenberg |
| 813 | newell-life-mrs-sherwood | Life of Mrs. Sherwood | 셔우드 부인의 삶 | Mrs. Sherwood | 1851 | 12 | Archive |
| 814 | rundle-charles-early-dawn | The Early Dawn | 이른 새벽 | Elizabeth Rundle Charles | 1896 | 12 | Archive |
| 815 | ridley-havergal-autobiography | Autobiography and Letters | 자서전과 편지 | Frances Ridley Havergal | 1879 | 15 | Archive |
| 816 | rossetti-face-of-deep | The Face of the Deep | 깊은 곳의 얼굴 | Christina Rossetti | 1894 | 15 | Archive |
| 817 | smith-unselfishness-of-god | The Unselfishness of God | 하나님의 비이기적 사랑 | Hannah Whitall Smith | 1911 | 12 | Gutenberg |
| 818 | catherine-siena-letters-sel | Letters of Catherine of Siena (selections) | 시에나의 카타리나 서신 (선집) | Catherine of Siena | 1380 | 15 | CCEL / Archive |
| 819 | julian-norwich-revelations-full | Revelations of Divine Love (full/long text) | 신적 사랑의 계시 (장문) | Julian of Norwich | ~1416 | 15 | CCEL |
| 820 | elizabeth-seton-sel | Selected Writings of Elizabeth Seton | 엘리자벳 시튼 선집 | Elizabeth Ann Seton | 1821 | 10 | Archive |
| 821 | gertrude-great-herald | Herald of Divine Love (selections) | 신적 사랑의 전령 (선집) | Gertrude the Great | 1302 | 10 | Archive |
| 822 | angela-foligno-memorial | The Memorial | 기록 | Angela of Foligno | 1309 | 10 | Archive |
| 823 | marguerite-porete-mirror-sel | Mirror of Simple Souls (selections) | 단순한 영혼의 거울 (선집) | Marguerite Porete | 1310 | 8 | Archive |
| 824 | hadewijch-visions-sel | Visions and Letters (selections) | 환시와 편지 (선집) | Hadewijch | ~1250 | 8 | Archive |
| 825 | beatrice-nazareth-seven-manners | Seven Manners of Loving | 사랑의 일곱 방식 | Beatrice of Nazareth | 1268 | 6 | Archive |

**소계**: 30권, ~366챕터, 예상 비용 ~$90

---

## 카테고리 27: 변증학 & 기독교 철학 확장 — 25권

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 826 | orr-christian-view-god | The Christian View of God and the World | 하나님과 세계에 대한 기독교적 관점 | James Orr | 1913 | 15 | Archive |
| 827 | orr-problem-ot | The Problem of the Old Testament | 구약의 문제 | James Orr | 1913 | 12 | Archive |
| 828 | orr-resurrection-jesus | The Resurrection of Jesus | 예수의 부활 | James Orr | 1913 | 12 | Archive |
| 829 | kuyper-encyclopedia-sel | Encyclopedia of Sacred Theology (sel.) | 성스러운 신학 백과사전 (선집) | Abraham Kuyper | 1920 | 15 | Archive |
| 830 | chesterton-napoleon-notting-hill | The Napoleon of Notting Hill | 노팅힐의 나폴레옹 | G.K. Chesterton | 1936 | 15 | Gutenberg |
| 831 | chesterton-flying-inn | The Flying Inn | 날아다니는 여관 | G.K. Chesterton | 1936 | 15 | Gutenberg |
| 832 | chesterton-man-who-was-thursday | The Man Who Was Thursday | 목요일이었던 사나이 | G.K. Chesterton | 1936 | 15 | Gutenberg |
| 833 | chesterton-club-queer-trades | The Club of Queer Trades | 별난 직업 클럽 | G.K. Chesterton | 1936 | 10 | Gutenberg |
| 834 | chesterton-varied-types | Varied Types | 다양한 유형 | G.K. Chesterton | 1936 | 12 | Gutenberg |
| 835 | chesterton-generally-speaking | Generally Speaking | 대체로 말하자면 | G.K. Chesterton | 1936 | 12 | Gutenberg |
| 836 | chesterton-autobiography | Autobiography | 자서전 | G.K. Chesterton | 1936 | 15 | Gutenberg / Archive |
| 837 | pascal-minor-works | Minor Works (selections) | 소품집 (선집) | Blaise Pascal | 1662 | 10 | Gutenberg |
| 838 | kierkegaard-fear-trembling | Fear and Trembling | 두려움과 떨림 | Soren Kierkegaard | 1855 | 10 | Archive |
| 839 | kierkegaard-sickness-unto-death | The Sickness Unto Death | 죽음에 이르는 병 | Soren Kierkegaard | 1855 | 12 | Archive |
| 840 | kierkegaard-attack-christendom | Attack upon Christendom (selections) | 기독교 세계 공격 (선집) | Soren Kierkegaard | 1855 | 12 | Archive |
| 841 | mozley-lectures-miracles | Lectures on Miracles | 기적에 관한 강의 | J.B. Mozley | 1878 | 10 | Archive |
| 842 | mansel-limits-religious-thought | The Limits of Religious Thought | 종교적 사고의 한계 | Henry Longueville Mansel | 1871 | 12 | Archive |
| 843 | pascal-mystery-jesus | The Mystery of Jesus | 예수의 신비 | Blaise Pascal | 1662 | 6 | Gutenberg |
| 844 | newman-grammar-assent | Grammar of Assent (selections) | 동의의 문법 (선집) | John Henry Newman | 1890 | 15 | Gutenberg / Archive |
| 845 | newman-apologia | Apologia Pro Vita Sua | 나의 생애 변증 | John Henry Newman | 1890 | 15 | Gutenberg |
| 846 | newman-idea-university-sel | The Idea of a University (selections) | 대학의 이념 (선집) | John Henry Newman | 1890 | 12 | Gutenberg |
| 847 | reid-common-sense-sel | Inquiry into the Human Mind (sel.) | 인간 정신에 대한 탐구 (선집) | Thomas Reid | 1796 | 12 | Archive / Gutenberg |
| 848 | james-william-varieties-rel | Varieties of Religious Experience (sel.) | 종교적 경험의 다양성 (선집) | William James | 1910 | 15 | Gutenberg |
| 849 | caird-evolution-religion | The Evolution of Religion | 종교의 진화 | Edward Caird | 1908 | 12 | Archive |
| 850 | illingworth-personality | Personality: Human and Divine | 인격: 인간과 신적 | J.R. Illingworth | 1915 | 10 | Archive |

**소계**: 25권, ~311챕터, 예상 비용 ~$75

---

## 카테고리 28: 찬송가 & 시 확장 — 20권

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 851 | sankey-gospel-hymns | Gospel Hymns and Sacred Songs | 복음 찬송가와 거룩한 노래 | Ira D. Sankey | 1908 | 15 | Archive / Gutenberg |
| 852 | sankey-my-life-sacred-song | My Life and the Story of the Gospel Hymns | 나의 삶과 복음 찬송의 이야기 | Ira D. Sankey | 1908 | 12 | Archive |
| 853 | bonar-god-plan-sel | God's Way of Peace | 하나님의 평화의 길 | Horatius Bonar | 1889 | 10 | CCEL / Archive |
| 854 | bonar-night-of-weeping | The Night of Weeping | 우는 밤 | Horatius Bonar | 1889 | 10 | CCEL / Archive |
| 855 | bonar-words-old-to-young | Words to the Young | 젊은이에게 보내는 말 | Horatius Bonar | 1889 | 8 | Archive |
| 856 | bliss-philip-gospel-songs | Gospel Songs | 복음 노래 | Philip Bliss | 1876 | 10 | Archive |
| 857 | montgomery-hymns | Poetical Works (selections) | 시선집 | James Montgomery | 1854 | 12 | Gutenberg / Archive |
| 858 | terstegen-spiritual-songs-sel | Spiritual Songs (selections) | 영적 노래 (선집) | Gerhard Tersteegen | 1769 | 10 | Archive |
| 859 | zinzendorf-hymns-sel | Hymns and Poems (selections) | 찬송가와 시 (선집) | Nikolaus von Zinzendorf | 1760 | 10 | Archive |
| 860 | baxter-poetical-fragments | Poetical Fragments | 시적 단편 | Richard Baxter | 1691 | 8 | CCEL / Archive |
| 861 | milton-samson-agonistes | Samson Agonistes | 투사 삼손 | John Milton | 1674 | 8 | Gutenberg |
| 862 | milton-comus | Comus | 코머스 | John Milton | 1674 | 6 | Gutenberg |
| 863 | milton-areopagitica | Areopagitica | 아레오파기티카 | John Milton | 1674 | 8 | Gutenberg |
| 864 | crashaw-poems-sel | Sacred Poems (selections) | 거룩한 시 (선집) | Richard Crashaw | 1649 | 10 | Gutenberg / Archive |
| 865 | vaughan-poems-sel | Sacred Poems (Silex Scintillans) | 부싯돌에서 나오는 불꽃 | Henry Vaughan | 1695 | 10 | Gutenberg |
| 866 | traherne-centuries-sel | Centuries of Meditations (selections) | 묵상의 세기 (선집) | Thomas Traherne | 1674 | 12 | Gutenberg / Archive |
| 867 | smart-jubilate-agno-sel | Jubilate Agno (selections) | 어린 양이여 기뻐하라 (선집) | Christopher Smart | 1771 | 8 | Gutenberg |
| 868 | thompson-hound-heaven | The Hound of Heaven and Other Poems | 천국의 사냥개와 기타 시 | Francis Thompson | 1907 | 8 | Gutenberg |
| 869 | hopkins-poems-sel | Selected Poems | 시선집 | Gerard Manley Hopkins | 1889 | 10 | Gutenberg / Archive |
| 870 | whittier-religious-poems | Religious Poems | 종교시 | John Greenleaf Whittier | 1892 | 12 | Gutenberg |

**소계**: 20권, ~197챕터, 예상 비용 ~$60

---

## 카테고리 29: 한국/동아시아 기독교 확장 — 20권

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 871 | gale-korean-sketches | Korean Sketches | 한국 스케치 | James Scarth Gale | 1937 | 15 | Gutenberg / Archive |
| 872 | gale-vanguard | Vanguard: A Tale of Korea | 선봉: 한국 이야기 | James Scarth Gale | 1937 | 12 | Archive |
| 873 | gale-korea-in-transition | Korea in Transition | 전환기의 한국 | James Scarth Gale | 1937 | 12 | Archive |
| 874 | hulbert-passing-of-korea | The Passing of Korea | 한국의 소멸 | Homer B. Hulbert | 1949 | 15 | Archive |
| 875 | hulbert-history-korea | The History of Korea | 한국의 역사 | Homer B. Hulbert | 1949 | 20 | Archive |
| 876 | jones-george-heber-korea | Korea: The Land, People and Customs | 한국: 나라, 사람, 풍속 | George Heber Jones | 1919 | 12 | Archive |
| 877 | baird-fifty-years-korea | Fifty Years in Korea | 한국에서의 오십 년 | Various | — | 15 | Archive |
| 878 | moffett-samuel-korean-mission | The Christians of Korea | 한국의 기독교인들 | Samuel A. Moffett | 1939 | 12 | Archive |
| 879 | blair-william-gold-in-korea | Gold in Korea | 한국의 금 | William Blair | 1957 | 12 | Archive |
| 880 | mckenzie-korea-tragedy | Korea's Fight for Freedom | 한국의 자유를 위한 투쟁 | F.A. McKenzie | 1920 | 15 | Gutenberg / Archive |
| 881 | morrison-memoirs | Memoirs of the Life of Robert Morrison | 로버트 모리슨 회고록 | E. Morrison | 1839 | 15 | Archive |
| 882 | medhurst-china | China: Its State and Prospects | 중국: 현황과 전망 | W.H. Medhurst | 1838 | 15 | Archive |
| 883 | nevius-demon-possession | Demon Possession and Allied Themes | 귀신 들림과 관련 주제 | John L. Nevius | 1893 | 12 | Archive |
| 884 | williams-middle-kingdom-sel | The Middle Kingdom (selections) | 중국 (선집) | S. Wells Williams | 1884 | 15 | Archive |
| 885 | verbeck-history-japan-protestant | History of Protestant Missions in Japan | 일본 개신교 선교 역사 | Various | — | 12 | Archive |
| 886 | kagawa-before-dawn | Before the Dawn | 새벽 이전 | Toyohiko Kagawa | 1960 | 15 | Archive |
| 887 | kagawa-brotherhood-economics | Brotherhood Economics | 형제애의 경제학 | Toyohiko Kagawa | 1960 | 10 | Archive |
| 888 | laufer-christian-movement-japan | The Christian Movement in Japan | 일본의 기독교 운동 | Various | — | 12 | Archive |
| 889 | swallen-william-baird-korea | William M. Baird of Korea | 한국의 윌리엄 베어드 | Various | — | 10 | Archive |
| 890 | korean-revival-1907 | The Korean Pentecost (1907 Revival Account) | 한국의 오순절 (1907년 부흥 기록) | W.N. Blair / Various | — | 10 | Archive |

**소계**: 20권, ~262챕터, 예상 비용 ~$60

---

## 카테고리 30: 청교도 & 개혁파 확장 — 30권

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 891 | rutherford-letters-v1 | Letters of Samuel Rutherford Vol.1 | 사무엘 러더포드 서신집 제1권 | Samuel Rutherford | 1661 | 20 | CCEL / Gutenberg |
| 892 | rutherford-letters-v2 | Letters of Samuel Rutherford Vol.2 | 사무엘 러더포드 서신집 제2권 | Samuel Rutherford | 1661 | 20 | CCEL / Gutenberg |
| 893 | rutherford-lex-rex-sel | Lex, Rex (selections) | 법, 왕 (선집) | Samuel Rutherford | 1661 | 15 | Archive |
| 894 | shepard-parable-ten-virgins | The Parable of the Ten Virgins | 열 처녀의 비유 | Thomas Shepard | 1649 | 15 | CCEL / Archive |
| 895 | shepard-sound-believer | The Sound Believer | 건전한 신자 | Thomas Shepard | 1649 | 12 | CCEL / Archive |
| 896 | shepard-sincere-convert | The Sincere Convert | 진실한 회심자 | Thomas Shepard | 1649 | 10 | CCEL / Archive |
| 897 | goodwin-patience-saints | Patience and Its Perfect Work | 인내와 그 완전한 역사 | Thomas Goodwin | 1680 | 10 | CCEL |
| 898 | goodwin-glory-gospel | The Glory of the Gospel | 복음의 영광 | Thomas Goodwin | 1680 | 12 | CCEL |
| 899 | goodwin-return-of-prayers | The Return of Prayers | 기도의 응답 | Thomas Goodwin | 1680 | 10 | CCEL |
| 900 | owen-death-of-death | The Death of Death in the Death of Christ | 그리스도의 죽음 안에서의 죽음의 죽음 | John Owen | 1683 | 15 | CCEL / Gutenberg |
| 901 | owen-justification | The Doctrine of Justification by Faith | 믿음으로 의롭다 하심의 교리 | John Owen | 1683 | 15 | CCEL |
| 902 | owen-person-of-christ | Meditations on the Person of Christ | 그리스도의 인격에 대한 묵상 | John Owen | 1683 | 12 | CCEL |
| 903 | owen-hebrews-sel-v1 | Exposition of Hebrews Vol.1 (selections) | 히브리서 주석 제1권 (선집) | John Owen | 1683 | 20 | CCEL |
| 904 | owen-hebrews-sel-v2 | Exposition of Hebrews Vol.2 (selections) | 히브리서 주석 제2권 (선집) | John Owen | 1683 | 20 | CCEL |
| 905 | brooks-unsearchable-riches | Unsearchable Riches of Christ | 그리스도의 측량할 수 없는 풍성 | Thomas Brooks | 1680 | 12 | CCEL |
| 906 | brooks-apples-gold | Apples of Gold | 금 사과 | Thomas Brooks | 1680 | 10 | CCEL |
| 907 | charnock-new-birth | The New Birth | 새로 태어남 | Stephen Charnock | 1680 | 10 | CCEL |
| 908 | charnock-sinfulness-sin | The Sinfulness and Cure of Thoughts | 생각의 죄스러움과 치유 | Stephen Charnock | 1680 | 10 | CCEL |
| 909 | flavel-england-duty-sel | England's Duty Under the Present Gospel Liberty (sel.) | 복음적 자유 아래서의 의무 (선집) | John Flavel | 1691 | 10 | CCEL |
| 910 | flavel-sacramental-meditations | Sacramental Meditations | 성례전 묵상 | John Flavel | 1691 | 10 | CCEL |
| 911 | watson-doctrine-of-repentance | The Doctrine of Repentance | 회개의 교리 | Thomas Watson | 1686 | 10 | CCEL |
| 912 | watson-godly-mans-picture | A Godly Man's Picture | 경건한 사람의 모습 | Thomas Watson | 1686 | 10 | CCEL |
| 913 | boston-crook-in-lot | The Crook in the Lot | 삶의 굴레 | Thomas Boston | 1732 | 10 | CCEL |
| 914 | boston-covenant-of-grace | The Covenant of Grace | 은혜의 언약 | Thomas Boston | 1732 | 10 | Archive |
| 915 | sibbes-fountain-sealed | The Fountain Sealed | 봉인된 샘 | Richard Sibbes | 1635 | 10 | CCEL |
| 916 | sibbes-glorious-freedom | Glorious Freedom | 영광스러운 자유 | Richard Sibbes | 1635 | 10 | CCEL |
| 917 | burroughs-gospel-reconciliation | Gospel Reconciliation | 복음적 화해 | Jeremiah Burroughs | 1646 | 10 | CCEL |
| 918 | manton-sermons-psalm119-sel | Sermons on Psalm 119 (selections) | 시편 119편 설교 (선집) | Thomas Manton | 1677 | 20 | CCEL |
| 919 | perkins-art-prophesying | The Art of Prophesying | 설교의 예술 | William Perkins | 1602 | 10 | CCEL / Archive |
| 920 | love-christopher-scottish-worthies | Scottish Worthies (selections) | 스코틀랜드의 위인들 (선집) | John Howie | 1793 | 15 | Archive / Gutenberg |

**소계**: 30권, ~379챕터, 예상 비용 ~$90

---

## 카테고리 31: 중세 추가 확장 — 20권

| # | slug | 영문 제목 | 한국어 제목 | 저자 | 사망 | 챕터 | 소스 |
|---|------|----------|-----------|------|------|------|------|
| 921 | bede-homilies-sel | Homilies (selections) | 설교집 (선집) | Venerable Bede | 735 | 12 | Archive |
| 922 | isidore-seville-etymologies-sel | Etymologies (selections) | 어원학 (선집) | Isidore of Seville | 636 | 10 | Archive |
| 923 | alcuin-letters-sel | Letters (selections) | 서신 선집 | Alcuin of York | 804 | 10 | Archive |
| 924 | peter-damian-letters-sel | Letters and Selected Writings | 서신과 저작 선집 | Peter Damian | 1072 | 12 | Archive |
| 925 | abelard-yes-no-sel | Sic et Non (selections) | 예와 아니오 (선집) | Peter Abelard | 1142 | 10 | Archive |
| 926 | abelard-ethics | Ethics (Scito Te Ipsum) | 윤리학 (너 자신을 알라) | Peter Abelard | 1142 | 10 | Archive |
| 927 | william-st-thierry-golden-epistle | The Golden Epistle | 황금 서신 | William of St. Thierry | 1148 | 10 | Archive |
| 928 | richard-st-victor-trinity | On the Trinity (De Trinitate) | 삼위일체론 | Richard of St. Victor | 1173 | 12 | Archive |
| 929 | richard-st-victor-twelve-patriarchs | The Twelve Patriarchs | 열두 족장 | Richard of St. Victor | 1173 | 10 | Archive |
| 930 | duns-scotus-sel | Selected Philosophical Writings | 철학 저작 선집 | Duns Scotus | 1308 | 10 | Archive |
| 931 | william-ockham-sel | Selected Philosophical Writings | 철학 저작 선집 | William of Ockham | 1347 | 10 | Archive |
| 932 | thomas-bradwardine-cause-god-sel | The Cause of God (selections) | 하나님의 원인 (선집) | Thomas Bradwardine | 1349 | 10 | Archive |
| 933 | wycliffe-select-english-works | Select English Works (selections) | 영어 저작 선집 | John Wycliffe | 1384 | 15 | Archive / CCEL |
| 934 | hus-de-ecclesia-sel | The Church (selections) | 교회론 (선집) | Jan Hus | 1415 | 12 | Archive |
| 935 | savonarola-sermons-sel | Selected Sermons and Writings | 설교와 저작 선집 | Girolamo Savonarola | 1498 | 10 | Archive |
| 936 | groote-following-christ | The Following of Christ | 그리스도를 따르며 | Gerard Groote | 1384 | 10 | Archive |
| 937 | gerson-consolation-theology-sel | On the Consolation of Theology (sel.) | 신학의 위로 (선집) | Jean Gerson | 1429 | 8 | Archive |
| 938 | nicolas-cusa-vision-god | The Vision of God | 하나님의 환시 | Nicholas of Cusa | 1464 | 12 | Archive |
| 939 | dominic-letters-sel | Selected Letters and Constitutions | 서신과 헌법 선집 | Dominic / Dominicans | 1221 | 8 | Archive |
| 940 | francis-de-sales-devout-life | Introduction to the Devout Life | 경건한 삶에 대한 입문 | Francis de Sales | 1622 | 15 | Gutenberg / CCEL |

**소계**: 20권, ~216챕터, 예상 비용 ~$60

---

## 총 요약

| 카테고리 | 권수 | 챕터 수 | 예상 비용 |
|----------|------|---------|-----------|
| 14. 교회사 텍스트 | 40 | 670 | $120 |
| 15. 동방교회 & 정교회 전통 | 30 | 392 | $90 |
| 16. 기독교 소설 & 알레고리 | 25 | 419 | $75 |
| 17. 기독교 윤리 & 사회사상 | 20 | 248 | $60 |
| 18. 목회신학 & 사역 지침서 | 25 | 313 | $75 |
| 19. 성경 배경 & 고고학 | 15 | 264 | $45 |
| 20. NPNF/ANF 시리즈 확장 | 60 | 850 | $180 |
| 21. 스펄전 확장 | 40 | 690 | $120 |
| 22. 성경 주석 확장 | 80 | 1,115 | $240 |
| 23. 추가 설교 모음집 | 40 | 532 | $120 |
| 24. 19~20세기 초 경건 서적 확장 | 60 | 685 | $180 |
| 25. 추가 종교개혁 & 신앙고백 | 20 | 229 | $60 |
| 26. 추가 선교사 전기 & 여성 신앙인 | 30 | 366 | $90 |
| 27. 변증학 & 기독교 철학 확장 | 25 | 311 | $75 |
| 28. 찬송가 & 시 확장 | 20 | 197 | $60 |
| 29. 한국/동아시아 기독교 확장 | 20 | 262 | $60 |
| 30. 청교도 & 개혁파 확장 | 30 | 379 | $90 |
| 31. 중세 추가 확장 | 20 | 216 | $60 |
| **합계** | **600** | **8,138** | **~$2,000** |

---

## 누적 총계 (전체 프로젝트)

| Phase | 권수 | 예상 비용 | 상태 |
|-------|------|-----------|------|
| Phase 1: 기초 도서 | 58 | ~$140 | 완료 |
| Phase 2: 확장 340권 | 340 | ~$1,020 | 완료 |
| **Phase 3: 추가 600권** | **600** | **~$2,000** | **카탈로그 작성** |
| **누적 총계** | **998** | **~$3,160** | — |

---

## 구현 우선순위

### 1순위 — 핵심 (200권, ~$600)
텍스트 확보 용이 + 영적 가치 최고 + 한국 교회 관련성 높음

- **교회사 핵심**: Eusebius (#341-343), Schaff 8권 (#362-369)
- **스펄전 확장**: New Park Street 6권 (#568-573), Treasury of David 확장 (#574-579)
- **JFB 주석 전체**: 22권 (#596-617) — 가장 실용적인 1권짜리 주석
- **칼빈 주석 확장**: 13권 (#649-661)
- **E.M. Bounds 기도 시리즈**: 7권 (#716-722) — 한국 교회에서 높은 인지도
- **한국 선교 기록**: #871-880 — 직접 관련
- **Andrew Murray 추가**: 8권 (#729-736) — 한국 교회 영성에 큰 영향
- **Owen/Rutherford 핵심**: 서신집 (#891-892), Death of Death (#900)
- **Morgan 복음서 강해**: 5권 (#676-680)
- **John Chrysostom 성경 강해**: #551-555

### 2순위 — 확장 (200권, ~$600)
- NPNF/ANF 시리즈 확장 (#496-555)
- 스펄전 MTP 추가 (#556-567)
- Keil & Delitzsch 구약 주석 (#618-631)
- Expositor's Bible 시리즈 (#638-648)
- 동방교회 전통 핵심 (#381-396)
- 청교도 추가 (#894-920)
- 여성 신앙인 (#809-825)

### 3순위 — 완성 (200권, ~$800)
- 나머지 성경 주석 (Ellicott, Gill, Poole, Clarke)
- 기독교 소설 전체
- 기독교 윤리 & 사회사상
- 변증학 확장
- 찬송가 & 시
- 중세 확장
- 설교 모음집 추가
- 목회신학 전체
- 경건 서적 잔여분

---

## 처리 참고사항

1. **소스 우선순위**: CCEL NPNF/ANF 텍스트 > Gutenberg 텍스트 > Archive 텍스트 > 기타 HTML
2. **대형 저작 분할**: Schaff 교회사, Spurgeon MTP, JFB 주석 등은 기존 `MAX_CHAPTER_WORDS=8000` 패턴 따라 분할
3. **메타데이터 형식**: 기존 `metadata.json` 패턴 준수
4. **slug 중복 확인**: Phase 1/2 카탈로그의 기존 slug과 중복 없음 (341번부터 시작)
5. **(sel.)로 표기된 항목**: 대형 저작에서 핵심 장만 선별 — 전체 번역이 아닌 선집
6. **저작권 주의**: Amy Carmichael(1951 사망), Watchman Nee(1972 사망) 등은 미국 1929년 이전 출판 기준 별도 확인 필요
7. **NPNF/ANF 볼륨 분할**: 한 볼륨이 너무 클 경우 저자별/주제별로 분할하여 처리
8. **한국 관련 자료**: Archive.org에서 "Korea" + "mission" 검색으로 추가 소스 확보 가능
