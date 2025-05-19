import * as Styles from './ItemSectionStyle.js';
import LostItemCard from './LostItemCard.js';

export default function LostItemsSection() {
  return (
    <Styles.ItemsWrapper>
      <LostItemCard
        title="흰색 우산"
        location="도서관"
        date="2025-04-15"
      />
      <LostItemCard
        title="검정 우산"
        location="도서관"
        date="2025-04-15"
      />
      <LostItemCard
        title="지갑"
        location="도서관"
        date="2025-04-15"
      />
      <LostItemCard
        title="노트북"
        location="도서관"
        date="2025-04-15"
      />
    </Styles.ItemsWrapper>
  );
}


