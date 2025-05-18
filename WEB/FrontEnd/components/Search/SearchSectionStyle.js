import styled from '@emotion/styled'

export const SearchWrapper = styled.div`
  box-sizing: border-box;
  width: 90%;
  max-width: 800px;
  background-color: white;
  border-radius: 16px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);

  display: flex;
  flex-direction: column;
`

export const SearchText = styled.div`
  color: #2D736C;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
`

export const SearchBox = styled.div`
  height: 150px;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: inset 0 0 3px rgba(0, 0, 0, 0.05);
  padding: 16px;
`

export const searchBoxDiv = styled.div`
  display: flex;
  flex-direction: row;
`

export const SearchBoxLabel = styled.div`
  width: 10%;
`

export const SearchBoxInputText = styled.input`
  width: 80%;
`

export const SearchBoxButton = styled.button`

`