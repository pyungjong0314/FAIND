import styled from '@emotion/styled';

export const SearchWrapper = styled.div`
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
  padding: 16px 32px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
`;

export const SearchTitle = styled.h2`
  font-size: 22px;
  color: #2d736c;
  text-align: center;
  margin-bottom: 24px;
`;

export const FormGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;

  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
`;

export const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

export const Label = styled.label`
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
`;

export const Input = styled.input`
  padding: 12px 12px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  outline: none;
  background-color: #fafafa;
  transition: border-color 0.2s;

  &:focus {
    border-color: #2d736c;
    background-color: #fff;
  }
`;

export const Select = styled.select`
  padding: 12px 12px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fafafa;
  transition: border-color 0.2s;
  outline: none;
  color: #333;

  &:focus {
    border-color: #2d736c;
    background-color: #fff;
  }

  /* ✅ 처음 선택 안 된 상태일 때 글자 흐리게 */
  &:invalid {
    color: #999;
  }
`;

export const ButtonRow = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 28px;
`;

export const Button = styled.button`
  padding: 14px 32px;
  background-color: #2d736c;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 12px;
  cursor: pointer;

  &:hover {
    background-color: #1f5e51;
  }
`;
