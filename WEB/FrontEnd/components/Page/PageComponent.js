import * as Styles from './PageStyle';

export default function Page({ totalPages, currentPage, onPageChange }) {
  const visibleCount = 5;
  let startPage = Math.max(currentPage - 2, 1);
  let endPage = startPage + visibleCount - 1;

  if (endPage > totalPages) {
    endPage = totalPages;
    startPage = Math.max(endPage - visibleCount + 1, 1);
  }

  const pages = [];
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return (
    <Styles.PageWrapper>
      {pages.map((pageNum) => (
        <Styles.PageButton
          key={pageNum}
          isActive={pageNum === currentPage}
          onClick={() => onPageChange(pageNum)}
        >
          {pageNum}
        </Styles.PageButton>
      ))}
    </Styles.PageWrapper>
  );
}
