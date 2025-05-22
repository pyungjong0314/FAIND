import * as Styles from "./WrapperStyle"
import { useState, useEffect } from 'react'
import { useQuery, gql } from '@apollo/client'
import PageSection from '../Page/PageComponent'
import LostItemsSection from "../Items/ItemSection"
import SearchSection from "../Search/SearchSection"

const PageCountGraphql = gql`
  query fetchPage($filter: LostFilterInput) {
    fetchPage(filter: $filter)
  }
`;

export default function WrapperSection({children}) {
    const [page, setPage] = useState(1)
    const [filter, setFilter] = useState({
        lost_name: '',
        lost_location: '',
        lost_date: ''
      });
    
    const {data} = useQuery(PageCountGraphql, {
        variables: {filter}
    })
    const [totalPage, setTotalPage] = useState(1)
    const pageSize = 4;

    useEffect(() => {
      if (data?.fetchPage) {
        const totalItemCount = data.fetchPage;
        const pageCount = Math.ceil(totalItemCount / pageSize);
        setTotalPage(pageCount);
      }
    }, [data]);

    const handleSearch = (newFilter) => {
        setFilter(newFilter);
        setPage(1);
    };

    return (
        <Styles.Wrapper>
            {children}
            
            <SearchSection onSearch={handleSearch} />

            <LostItemsSection
                currentPage={page}
                pageSize={pageSize}
                filter={filter}
            />

            <PageSection
                totalPages={totalPage}
                currentPage={page}
                onPageChange={(newPage) => setPage(newPage)}
            />
        </Styles.Wrapper>
    )
}