import * as Styles from './ItemSectionStyle.js';
import LostItemCard from './LostItemCard.js';
import { useQuery, gql } from '@apollo/client';

const PageLostGraphql = gql`
  query FetchPageLost($page: Int!, $pageSize: Int!, $filter: LostFilterInput) {
    fetchPageLost(page: $page, pageSize: $pageSize, filter: $filter) {
        id
        lost_name
        lost_location
        lost_date
      }
    }
`

export function formatDate(timestamp) {

  return new Date(Number(timestamp)).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
}

export default function LostItemsSection({currentPage, pageSize, filter}) {
  const {data} = useQuery(PageLostGraphql, {
    variables: {
      page: currentPage,
      pageSize: pageSize,
      filter: filter
    }
  })

  return (    
    <Styles.ItemsWrapper>
      {data?.fetchPageLost.map((item) => (
        <LostItemCard
          key={item.id}
          title={item.lost_name}
          location={item.lost_location}
          date={formatDate(item.lost_date)}
        />
      ))}
    </Styles.ItemsWrapper>
  );
}


