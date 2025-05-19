import * as Styles from './SearchSectionStyle';

export default function SearchSectionUI() {
  return (
    <Styles.SearchWrapper>
      <Styles.SearchTitle>습득물 상세 검색</Styles.SearchTitle>

      <Styles.FormGrid>
        <Styles.InputGroup>
          <Styles.Label>이름</Styles.Label>
          <Styles.Input placeholder="예: 검정색 우산" />
        </Styles.InputGroup>

        <Styles.InputGroup>
          <Styles.Label>카테고리</Styles.Label>
          <Styles.Input placeholder="예: 우산" />
        </Styles.InputGroup>

        <Styles.InputGroup>
          <Styles.Label>날짜</Styles.Label>
          <Styles.Input type="date" />
        </Styles.InputGroup>

        <Styles.InputGroup>
          <Styles.Label>장소</Styles.Label>
          <Styles.Input placeholder="장소를 입력하세요" />
        </Styles.InputGroup>
      </Styles.FormGrid>

      <Styles.ButtonRow>
        <Styles.Button>검색</Styles.Button>
      </Styles.ButtonRow>
    </Styles.SearchWrapper>
  );
}
