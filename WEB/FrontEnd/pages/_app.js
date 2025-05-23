import '../styles/globals.css';
import {ApolloClient, InMemoryCache, ApolloProvider} from "@apollo/client"

const client = new ApolloClient({
  uri: 'http://223.194.45.67:8003', // ✅ 꼭 uri!
  cache: new InMemoryCache(),
});

export default function App({ Component, pageProps }) {

  return (
    <ApolloProvider client={client}>
      <Component {...pageProps} />
    </ApolloProvider>
  );
}
