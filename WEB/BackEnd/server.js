import { sequelize } from './sequelizeInstance.js';
import { ApolloServer } from '@apollo/server';
import {startStandaloneServer} from '@apollo/server/standalone';
import { personQuery, fetchPersons, createPerson } from './Controller/personController.js';
import { lostQuery, fetchAllLost, createLost, fetchPage, fetchPageLost } from './Controller/lostController.js';


// API-DOCS
const typeDefs = `#graphql
    ${personQuery}
    ${lostQuery}
`;

// API
const resolvers = {
    Query: {
        fetchPersons,
        fetchAllLost,
        fetchPage,
        fetchPageLost
    },

    Mutation: {
        createPerson,
        createLost
    }
};

const server = new ApolloServer({
    typeDefs,
    resolvers,
    cors: true,

    // cors: {
    //     origin: ["http://naver.com"]
    // }
});

async function initialize() {
  try {
    await sequelize.sync({ alter: true });

    console.log('DB 접속에 성공했습니다!');
  } catch (error) {
    console.error('DB 접속에 실패했습니다!');
    console.error('원인:', error);
  }
}

initialize();

startStandaloneServer(server).then(()=>{
    console.log("서버가 실행되었습니다!");
});