import * as Styles from './SearchSectionStyle';

export default function SearchSectionUI({ filter, setFilter, onClickSearch }) {
  return (
    <Styles.SearchWrapper>
      <Styles.SearchTitle>습득물 상세 검색</Styles.SearchTitle>

      <Styles.FormGrid>
        <Styles.InputGroup>
          <Styles.Label>이름</Styles.Label>
          <Styles.Input
            name="lost_name"
            placeholder="예: 검정색 우산"
            value={filter.lost_name}
            onChange={(e) => setFilter({ ...filter, lost_name: e.target.value })}
          />
        </Styles.InputGroup>

        <Styles.InputGroup>
          <Styles.Label>상태</Styles.Label>
          <Styles.Select
            name="status"
            value={filter.status}
            onChange={(e) => setFilter({ ...filter, status: e.target.value })}
            required
          >
            <option value="" disabled>
              선택하세요
            </option>
            <option value="found">보관</option>
            <option value="returned">완료</option>
          </Styles.Select>
        </Styles.InputGroup>

        <Styles.InputGroup>
          <Styles.Label>날짜</Styles.Label>
          <Styles.Input
            type="date"
            name="lost_date"
            value={filter.lost_date}
            onChange={(e) => setFilter({ ...filter, lost_date: e.target.value })}
          />
        </Styles.InputGroup>

        <Styles.InputGroup>
          <Styles.Label>장소</Styles.Label>
          <Styles.Input
            name="lost_location"
            placeholder="장소를 입력하세요"
            value={filter.lost_location}
            onChange={(e) => setFilter({ ...filter, lost_location: e.target.value })}
          />
        </Styles.InputGroup>
      </Styles.FormGrid>

      <Styles.ButtonRow>
        <Styles.Button onClick={onClickSearch}>검색</Styles.Button>
      </Styles.ButtonRow>
    </Styles.SearchWrapper>
  );
}