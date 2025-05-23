import styled from '@emotion/styled';

export const PageWrapper = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 24px;
  gap: 8px;
`;

export const PageButton = styled.button`
  padding: 8px 14px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  
  background-color: ${(props) => (props.isActive ? '#2d736c' : '#e0e0e0')};
  color: ${(props) => (props.isActive ? '#fff' : '#333')};
  font-weight: ${(props) => (props.isActive ? 'bold' : 'normal')};
  transition: background-color 0.2s;

  &:hover {
    background-color: ${(props) => (props.isActive ? '#1f5e51' : '#d0d0d0')};
  }
`;
