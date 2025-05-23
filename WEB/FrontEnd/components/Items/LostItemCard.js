import * as Styles from './ItemSectionStyle';

export default function LostItemCard({ title, location, date }) {
  return (
    <Styles.Item>
      <Styles.ItemImage />
      <Styles.ItemText>
        <div>
          <Styles.ItemTextTitle>{title}</Styles.ItemTextTitle>
          <Styles.ItemTextDetail>{location}에서 {title}을(를) 발견하였습니다.</Styles.ItemTextDetail>
        </div>

        <Styles.ItemMeta>
          {date} 
        </Styles.ItemMeta>
      </Styles.ItemText>
    </Styles.Item>
  );
}