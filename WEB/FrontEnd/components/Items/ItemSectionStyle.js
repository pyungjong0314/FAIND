import styled from '@emotion/styled';

export const ItemsWrapper = styled.div`
  width: 100%;
  max-width: 800px;
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
`;

export const Item = styled.div`
  display: flex;
  align-items: flex-start;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  padding: 24px;
  transition: box-shadow 0.2s ease;

  &:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  }

  @media (max-width: 600px) {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px;
  }
`;

export const ItemImage = styled.div`
  width: 120px;
  height: 120px;
  background-color: #e0e0e0;
  border-radius: 12px;
  flex-shrink: 0;
  margin-right: 24px;

  @media (max-width: 600px) {
    margin-right: 0;
    margin-bottom: 14px;
  }
`;

export const ItemText = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 상단 정보 + 하단 날짜/시간 분리 */
  flex: 1;                         /* 남은 영역 다 차지 */
  min-height: 120px;              /* 높이 확보 */
`;

export const ItemTextTitle = styled.div`
  font-size: 18px;
  font-weight: 700;
  color: #2d736c;
  margin-bottom: 10px;
`;

export const ItemTextDetail = styled.div`
  font-size: 15px;
  color: #444;
  line-height: 1.7;
`;

export const ItemMeta = styled.div`
  font-size: 13px;
  color: #777;
  align-self: flex-end; /* 오른쪽 정렬 */
`;