import styled from '@emotion/styled'

export const ItemsWrapper = styled.div`
  width: 90%;
  max-width: 800px;
  margin-top: 30px;

  display: flex;
  flex-direction: column;
  gap: 16px;
`

export const Item = styled.div`
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.07);
  padding: 16px;

  display: flex;
  align-items: center;
`

export const ItemImage = styled.div`
  height: 100px;
  width: 100px;
  background-color: #eee;
  border-radius: 10px;
  margin-right: 20px;
  flex-shrink: 0;
`

export const ItemText = styled.div`
  display: flex;
  flex-direction: column;
`

export const ItemTextTitle = styled.div`
  color: #2D736C;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 6px;
`

export const ItemTextDetail = styled.div`
  color: #444;
  font-size: 14px;
  line-height: 1.4;
`