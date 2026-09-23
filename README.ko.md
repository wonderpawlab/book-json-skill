# Book JSON Skill

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

영어 단어 목록, PDF, 스캔 문서, 사진으로 나만의 단어장 `book.json`을 만듭니다. 뜻풀이에 사용할 언어를 지정하면 AI가 대상 어휘를 추출하고 예문과 번역을 추가한 뒤, 프로젝트에 포함된 템플릿에 따라 결과를 확인합니다.

이 프로젝트는 독립형 Python 검증 도구가 포함된 **AI 에이전트 스킬**입니다. 콘텐츠 생성과 이미지·PDF 읽기는 스킬을 실행하는 에이전트의 기능을 사용합니다. 검증 도구만 실행해서는 어휘를 추출하거나 번역하거나 생성할 수 없습니다.

## 생성할 수 있는 내용

- 영어, 중국어 간체, 중국어 번체, 일본어, 한국어 등 지정한 언어로 작성한 뜻풀이.
- **모든 의미 그룹**에 해당하는 영어 예문과 지정한 언어의 번역.
- 선택적인 단원 구성. `Lesson 2`나 `Unit 1 / Lesson 2`는 `word.unit`에 저장하며, 단원 구분이 없는 단어장은 이 필드를 생략합니다.
- 문자열 형식의 연속된 ID. 같은 단원 안의 중복 항목은 병합하고, 서로 다른 단원의 항목은 별도 레코드로 유지합니다.
- 확인할 수 없는 발음기호는 빈 문자열로 두고, 누락된 정보는 파일 밖에서 안내합니다.
- 새 단어장 또는 기존 단어장을 제공해 어휘를 추가한 통합 단어장.

출력 형식은 이 프로젝트의 [단어장 형식 명세](skills/book-json/references/book_template.md)를 지원하는 앱을 위한 것입니다. 모든 단어 학습 프로그램에서 통용되는 교환 형식은 아닙니다. 결과를 가져오는 앱이 지원하는 뜻풀이 언어는 이 스킬이 생성할 수 있는 언어보다 적을 수 있습니다.

## 설치

이 저장소를 다운로드해 압축을 풀거나 복제한 뒤, 사용하는 도구에 맞는 설치 방법을 선택하세요. 복사할 대상은 다운로드한 프로젝트의 **`skills/book-json` 폴더 전체**입니다. 보통 개인용으로 설치하며, 특정 프로젝트에서만 사용하려면 해당 프로젝트 안에 설치합니다.

Windows 표는 Windows에서 도구를 직접 실행할 때의 경로입니다. WSL 안에서 실행한다면 Windows 사용자 폴더가 아니라 WSL의 Linux 사용자 홈 디렉터리를 사용하세요.

### Claude Code

#### Windows

| 사용 범위 | 최종 설치 위치 | 전체 경로 예시 |
| --- | --- | --- |
| 개인용 (권장) | `%USERPROFILE%\.claude\skills\book-json\` | `C:\Users\alice\.claude\skills\book-json\` |
| 특정 프로젝트 | `<프로젝트 루트>\.claude\skills\book-json\` | `C:\Projects\my-study\.claude\skills\book-json\` |

파일 탐색기로 빠르게 설치하려면 다음 순서로 진행하세요.

1. `Win + E`를 눌러 파일 탐색기를 열고, `Ctrl + L`로 주소 표시줄을 선택합니다.
2. `%USERPROFILE%`을 붙여 넣고 Enter를 누르면 현재 사용자의 홈 폴더가 열립니다.
3. 홈 폴더에 `.claude` 폴더를 만들고, 그 안에 `skills` 폴더를 만듭니다. 이미 있다면 기존 폴더를 사용하세요. `%USERPROFILE%\.claude\skills`를 주소 표시줄에 붙여 넣으면 이 폴더로 바로 이동할 수 있습니다.
4. 다운로드 후 압축을 푼 프로젝트에서 `skills` 안의 **`book-json` 폴더 전체**를 위의 `skills` 폴더에 복사합니다.
5. `%USERPROFILE%\.claude\skills\book-json\SKILL.md`가 있는지 확인합니다.

`%USERPROFILE%`은 파일 탐색기에서 현재 사용자의 홈 경로로 자동 해석되므로 직접 바꿀 필요가 없습니다. 위 예시의 `alice`는 사용자 이름, `my-study`는 프로젝트 이름입니다. 전체 경로 예시를 사용할 때는 본인의 실제 경로로 바꾸세요. 프로젝트에 설치할 경우에도 해당 프로젝트 루트에 `.claude\skills`를 만든 뒤 `book-json` 폴더 전체를 복사합니다.

#### macOS

| 사용 범위 | 최종 설치 위치 | 전체 경로 예시 |
| --- | --- | --- |
| 개인용 (권장) | `~/.claude/skills/book-json/` | `/Users/alice/.claude/skills/book-json/` |
| 특정 프로젝트 | `<프로젝트 루트>/.claude/skills/book-json/` | `/Users/alice/Projects/my-study/.claude/skills/book-json/` |

Finder로 빠르게 설치하려면 다음 순서로 진행하세요.

1. Finder에서 `Command + Shift + G`를 누르고 `~/.claude/skills/`를 입력한 뒤 Return을 누릅니다.
2. 폴더가 아직 없으면 터미널에서 아래 두 줄을 실행하여 폴더를 만들고 엽니다.

   ```sh
   mkdir -p "$HOME/.claude/skills"
   open "$HOME/.claude/skills"
   ```

3. 다운로드 후 압축을 푼 프로젝트에서 `skills` 안의 **`book-json` 폴더 전체**를 열린 `skills` 폴더에 복사합니다.
4. `~/.claude/skills/book-json/SKILL.md`가 있는지 확인합니다. Finder에서 숨김 폴더를 보려면 `Command + Shift + .`을 누르세요.

`~`는 현재 사용자의 홈 폴더를 뜻하므로 직접 바꿀 필요가 없습니다. 위 예시의 `alice`와 `my-study`는 예시 이름이므로 전체 경로 예시를 사용할 때는 본인의 실제 경로로 바꾸세요. 프로젝트에 설치할 경우에도 해당 프로젝트 루트에 `.claude/skills`를 만든 뒤 `book-json` 폴더 전체를 복사합니다.

Claude Code에서는 **`/book-json`**으로 호출합니다. [Claude Code 공식 스킬 문서](https://code.claude.com/docs/en/skills)를 참고하세요.

### Codex

#### Windows

| 사용 범위 | 최종 설치 위치 | 전체 경로 예시 |
| --- | --- | --- |
| 개인용 (권장) | `%USERPROFILE%\.agents\skills\book-json\` | `C:\Users\alice\.agents\skills\book-json\` |
| 특정 프로젝트 | `<프로젝트 루트>\.agents\skills\book-json\` | `C:\Projects\my-study\.agents\skills\book-json\` |

파일 탐색기로 빠르게 설치하려면 다음 순서로 진행하세요.

1. `Win + E`를 눌러 파일 탐색기를 열고, `Ctrl + L`로 주소 표시줄을 선택합니다.
2. `%USERPROFILE%`을 붙여 넣고 Enter를 누르면 현재 사용자의 홈 폴더가 열립니다.
3. 홈 폴더에 `.agents` 폴더를 만들고, 그 안에 `skills` 폴더를 만듭니다. 이미 있다면 기존 폴더를 사용하세요. `%USERPROFILE%\.agents\skills`를 주소 표시줄에 붙여 넣으면 이 폴더로 바로 이동할 수 있습니다.
4. 다운로드 후 압축을 푼 프로젝트에서 `skills` 안의 **`book-json` 폴더 전체**를 위의 `skills` 폴더에 복사합니다.
5. `%USERPROFILE%\.agents\skills\book-json\SKILL.md`가 있는지 확인합니다.

`%USERPROFILE%`은 파일 탐색기에서 현재 사용자의 홈 경로로 자동 해석되므로 직접 바꿀 필요가 없습니다. 위 예시의 `alice`는 사용자 이름, `my-study`는 프로젝트 이름입니다. 전체 경로 예시를 사용할 때는 본인의 실제 경로로 바꾸세요. 프로젝트에 설치할 경우에도 해당 프로젝트 루트에 `.agents\skills`를 만든 뒤 `book-json` 폴더 전체를 복사합니다.

#### macOS

| 사용 범위 | 최종 설치 위치 | 전체 경로 예시 |
| --- | --- | --- |
| 개인용 (권장) | `~/.agents/skills/book-json/` | `/Users/alice/.agents/skills/book-json/` |
| 특정 프로젝트 | `<프로젝트 루트>/.agents/skills/book-json/` | `/Users/alice/Projects/my-study/.agents/skills/book-json/` |

Finder로 빠르게 설치하려면 다음 순서로 진행하세요.

1. Finder에서 `Command + Shift + G`를 누르고 `~/.agents/skills/`를 입력한 뒤 Return을 누릅니다.
2. 폴더가 아직 없으면 터미널에서 아래 두 줄을 실행하여 폴더를 만들고 엽니다.

   ```sh
   mkdir -p "$HOME/.agents/skills"
   open "$HOME/.agents/skills"
   ```

3. 다운로드 후 압축을 푼 프로젝트에서 `skills` 안의 **`book-json` 폴더 전체**를 열린 `skills` 폴더에 복사합니다.
4. `~/.agents/skills/book-json/SKILL.md`가 있는지 확인합니다. Finder에서 숨김 폴더를 보려면 `Command + Shift + .`을 누르세요.

`~`는 현재 사용자의 홈 폴더를 뜻하므로 직접 바꿀 필요가 없습니다. 위 예시의 `alice`와 `my-study`는 예시 이름이므로 전체 경로 예시를 사용할 때는 본인의 실제 경로로 바꾸세요. 프로젝트에 설치할 경우에도 해당 프로젝트 루트에 `.agents/skills`를 만든 뒤 `book-json` 폴더 전체를 복사합니다.

Codex CLI/IDE에서는 **`$book-json`**으로 호출합니다. [Codex 공식 로컬 스킬 문서](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)를 참고하세요.

### 기타 도구

- **`SKILL.md`를 지원하는 도구**: 해당 도구의 공식 문서에서 설치 위치와 활성화·호출 방법을 확인하고, `skills/book-json` 폴더 전체를 복사하세요. 모든 도구에 공통으로 적용되는 설치 경로나 호출 명령은 없습니다.
- **스킬 기능이 없는 도구**: 파일을 읽을 수 있는 AI에 `SKILL.md`와 `assets/`, `references/`, `scripts/`를 함께 제공하고 스킬의 지침에 따라 `book.json`을 생성해 달라고 요청할 수 있습니다. 이는 수동 사용 방법이며, `/book-json`이나 `$book-json`을 명령으로 사용할 수 있게 되는 것은 아닙니다. Python을 실행할 수 없다면 자동 검증을 수행하지 않았음을 명시해야 합니다.

### 설치 확인 및 실행 조건

복사한 `book-json` 폴더 바로 아래에 `SKILL.md`가 있어야 합니다. `book-json/book-json/SKILL.md`처럼 폴더를 중복으로 넣지 마세요. `SKILL.md`만 복사하면 템플릿과 검증 도구가 빠집니다.

실행 조건:

- 에이전트가 제공된 파일을 읽고 결과를 저장할 수 있어야 합니다. 사진과 스캔 PDF에는 이미지 인식 또는 OCR이, 텍스트 PDF에는 문서 읽기 도구가 필요합니다. 이 저장소에는 OCR 엔진이 포함되어 있지 않습니다.
- 자동 검증에는 **Python 3.10 이상**이 필요하며, 검증 도구는 **서드파티 패키지에 의존하지 않습니다**. Python이 없으면 에이전트가 수동으로 확인할 수 있지만, 자동 검증을 실행하지 못했다는 사실을 알려야 합니다.
- 이 프로젝트 전용 API 키는 필요하지 않습니다. 모델 사용과 도구 설정은 이용하는 AI 에이전트의 환경을 따릅니다.

## 사용법

**Claude Code에서는 `/book-json`, Codex CLI/IDE에서는 `$book-json`**으로 호출합니다. 다른 도구에서는 해당 도구의 활성화 방법이나 위의 수동 사용 방법을 따르세요. **뜻풀이 언어와 단어 또는 원본 파일을 모두** 제공하세요. 둘 중 하나가 빠지면 스킬이 질문합니다. 언어를 ‘중국어’라고만 지정하면 간체인지 번체인지 확인합니다.

아래 세 예시는 Codex 호출 방식으로 작성했습니다. Claude Code에서는 첫 줄을 `/book-json`으로 바꾸세요. 다른 도구에서는 해당 도구의 호출 방법에 맞게 사용하세요.

### 단어 직접 입력

```text
$book-json
뜻풀이 언어: 한국어.
단어: apple, borrow, look after.
난이도: A2.
book.json을 생성해 주세요. 이 단어들은 Unit이나 Lesson으로 구분하지 않습니다.
```

### PDF 또는 사진 사용

원본 파일을 첨부한 뒤 다음과 같이 요청합니다.

```text
$book-json
뜻풀이 언어: 한국어.
첨부한 PDF의 4~8쪽에 있는 단어 목록과 첨부 사진 두 장의 어휘를 사용해 주세요.
자료에 표시된 Unit/Lesson 제목을 유지하고 영어 예문과 한국어 번역을 추가해 book.json을 만들어 주세요.
```

페이지 범위, 난이도, 단원 이름, 출력 디렉터리는 선택 사항입니다. 스킬은 읽는 순서와 추출 누락 여부를 확인합니다. 읽을 수 없는 항목이 있으면 더 선명하게 잘라낸 이미지나 페이지를 제공해야 완성된 단어장을 전달할 수 있습니다. 명확한 단어 목록이 없는 일반 글에서는 어떤 단어를 수집할지 지정하세요.

### 기존 단어장 확장

```text
$book-json
뜻풀이 언어: 한국어.
첨부한 기존 book.json에 이 사진의 어휘를 추가해 주세요.
통합한 결과를 book.extended.json으로 저장해 주세요.
```

기존의 올바른 내용은 유지합니다. 같은 단원에서 철자가 같은 항목은 의미를 빠뜨리지 않고 병합합니다. 다른 단원의 항목은 각각 유지합니다. 기존 단어장의 언어가 지정한 언어와 다르면 처리 방법을 확인합니다. 덮어쓰기를 요청하지 않는 한 새 파일에 저장합니다.

## 출력 형식

```json
[
  {
    "word": {
      "wordHead": "apple",
      "wordId": "1",
      "content": {
        "usphone": "",
        "ukphone": "",
        "trans": [
          {
            "tranCn": "사과",
            "pos": "n",
            "sentence_example": "I eat an apple after lunch.\n나는 점심을 먹은 후에 사과 한 개를 먹습니다."
          }
        ]
      }
    }
  }
]
```

`tranCn`은 기존 형식에서 이어진 필드 이름으로, **선택한 언어의 뜻풀이**를 담습니다. 이름을 바꾸거나 `language` 메타데이터를 추가하지 마세요. 예문 필드는 JSON을 파싱한 뒤 정확히 두 줄이어야 합니다. 뜻풀이 언어가 영어이면 두 번째 줄에는 같은 의미를 다른 표현으로 쓴 영어 문장을 넣습니다.

**어떤 단어장이든 `unit`을 생략할 수 있습니다.** 원본 자료의 Lesson은 `unit`에 저장하며, 별도의 `lesson` 필드를 추가하지 않습니다. 원본의 의미와 품사는 유지하고, 예문이 없으면 AI가 작성합니다. 발음기호는 확인된 경우에만 채웁니다. 문장부호에 따른 의미 분리와 단원별 중복 병합 규칙은 [전체 형식 명세](skills/book-json/references/book_template.md)를 참고하세요.

예제: [English](examples/book.en.json), [繁體中文](examples/book.zh-Hant.json), [简体中文](examples/book.zh-Hans.json), [日本語](examples/book.ja.json), [한국어](examples/book.ko.json), [선택적인 Lesson/Unit 구분](examples/book.lessons.json).

## 검증

저장소 루트 디렉터리에서 실행합니다.

```sh
python skills/book-json/scripts/validate_book.py examples/book.ja.json
python skills/book-json/scripts/validate_book.py /path/to/book.json --json
```

환경에 따라 `python`을 `python3` 같은 Python 3 실행 명령으로 바꾸세요. 여러 파일 경로를 함께 전달할 수 있습니다. 종료 코드 `0`은 모든 파일의 통과를, `1`은 검증 실패를 뜻합니다. `--json`은 기계가 읽을 수 있는 보고서를 출력합니다. 검증 도구는 파일을 읽기만 하며 수정하지 않습니다.

엄격한 필드·자료형 검사, 필수 예문, 연속된 ID, 중복 항목과 의미, 남아 있는 자리 표시자, 발음기호 바깥의 구분 기호, UTF-8 JSON, 가져오기 제한인 **100,000개 레코드 / 30 MiB** 등을 확인합니다. [JSON Schema](skills/book-json/assets/book.schema.json)로 편집기에서도 검사할 수 있습니다.

구조 검증만으로는 OCR 정확도, 원본 내용의 누락 여부, 지정한 언어 사용 여부, 번역 품질, 예문이 해당 의미를 제대로 보여 주는지를 판단할 수 없습니다. 스킬은 에이전트가 이 내용을 별도로 검토하도록 요구합니다.

## 프로젝트 구조

```text
skills/book-json/
  SKILL.md                         에이전트 작업 절차와 적용 조건
  agents/openai.yaml               표시용 메타데이터
  assets/book.template.json        생성 템플릿
  assets/book.schema.json          JSON Schema
  references/book_template.md      전체 형식 명세
  references/source-extraction.md  PDF·사진 읽기 절차
  references/extending-books.md    기존 단어장 확장 시 병합 규칙
  scripts/validate_book.py         표준 라이브러리 기반 읽기 전용 검증 도구
examples/                         직접 작성한 예제 단어장
tests/                            자동 검증 테스트
.github/workflows/validate.yml    Linux/Windows CI
```

## 개발 및 공개

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

개발 의존성은 테스트와 메타데이터·Schema 검사에만 사용합니다. 검증 도구 실행에는 이러한 패키지가 필요하지 않습니다. CI는 테스트를 실행하고 예제 단어장을 검증합니다.

GitHub에 공개할 때는 **이 디렉터리를 독립 저장소의 루트**로 사용하세요. Flutter 프로젝트, 원본 어휘 데이터, 로컬 컴퓨터 경로, 외부 프로젝트 파일에 의존하지 않습니다. 배포할 때는 스킬 폴더 전체를 유지하세요. 형식을 바꿀 때는 명세, Schema, 검증 도구, 예제, 테스트를 함께 업데이트하고, 다섯 언어의 README 내용도 일치하도록 유지하세요.

로컬 작업용 `inputs/`와 `outputs/`는 Git 추적 대상에서 제외되어 있습니다. 업로드한 자료는 선택한 AI 제품과 그 도구에서 처리합니다. 검증 도구 자체는 네트워크 요청을 보내지 않습니다. 비공개 원본 자료를 저장소에 커밋하지 마세요.

## 라이선스

[MIT](LICENSE). 포함된 예제는 직접 작성한 샘플입니다. 이 라이선스는 프로젝트에 적용되며, 사용자가 제공하는 제삼자의 도서나 사진 등에는 적용되지 않습니다.
