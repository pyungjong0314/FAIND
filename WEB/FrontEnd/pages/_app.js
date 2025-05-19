import '../styles/globals.css';
import {ApolloClient, InMemoryCache, ApolloProvider} from "@apollo/client"

export default function App({ Component, pageProps }) {
  const client = new ApolloClient({
    url: "http://localhost:4000/",
    cache: new InMemoryCache() // 컴퓨터 메모리에 백엔드 데이터 임시 저장
  })

  return <Component {...pageProps} />;
}
