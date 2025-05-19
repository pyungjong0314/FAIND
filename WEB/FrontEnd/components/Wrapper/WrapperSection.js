import * as Styles from "./WrapperStyle"
import { useState, useEffect } from 'react'
import { useQuery, gql } from '@apollo/client'
import PageSection from '../Page/PageComponent'
import LostItemsSection from "../Items/ItemSection"

const PageCountGraphql = gql`
    query {
        fetchPage
    }   
`;

export default function WrapperSection({children}) {
    const [page, setPage] = useState(1)
    const {data} = useQuery(PageCountGraphql)
    const [totalPage, setTotalPage] = useState(1)
    const pageSize = 4;

    useEffect(() => {
      if (data?.fetchPage) {
        const totalItemCount = data.fetchPage;
        const pageCount = Math.ceil(totalItemCount / pageSize);
        setTotalPage(pageCount);
      }
    }, [data]);

    return (
        <Styles.Wrapper>
            {children}
            
            <LostItemsSection
                currentPage={page}
                pageSize={pageSize}
            />

            <PageSection
                totalPages={totalPage}
                currentPage={page}
                onPageChange={(newPage) => setPage(newPage)}
            />
        </Styles.Wrapper>
    )
}