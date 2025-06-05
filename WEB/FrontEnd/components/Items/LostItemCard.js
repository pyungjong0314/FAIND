import * as Styles from './ItemSectionStyle';

export default function LostItemCard({ title, location, date, image }) {
  const isValidImage = image && image !== 'null' && image !== 'undefined';

  // 프록시 URL 생성
  const proxiedImage = isValidImage
    ? `https://images.weserv.nl/?url=${encodeURIComponent(image)}`
    : null;
  
  return (
    <Styles.Item>
      <Styles.ItemImage image={proxiedImage} />
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