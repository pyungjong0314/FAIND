import '../styles/globals.css';
import {ApolloClient, InMemoryCache, ApolloProvider} from "@apollo/client"

const client = new ApolloClient({
  uri: 'http://localhost:4000/graphql', // ✅ 꼭 uri!
  cache: new InMemoryCache(),
});

export default function App({ Component, pageProps }) {

  return (
    <ApolloProvider client={client}>
      <Component {...pageProps} />
    </ApolloProvider>
  );
}
