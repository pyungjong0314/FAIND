import { useState } from 'react';
import SearchSectionUI from './SearchSectionUI';

export default function SearchSection({ onSearch }) {
  const [filter, setFilter] = useState({
    lost_name: '',
    lost_location: '',
    lost_date: ''
  });

  const handleSearch = () => {
    onSearch(filter); // ✅ WrapperSection으로 filter 전달
  };

  return (
    <SearchSectionUI
      filter={filter}
      setFilter={setFilter}
      onClickSearch={handleSearch} // ✅ 전달
    />
  );
}
