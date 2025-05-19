import { Lost } from "../Entity/lost.js"

export const lostQuery = `
    type Person {
        id: Int
        input_time: String
    }

    enum statusEnum {
        found
        returned
    }

    type Lost {
        id: Int
        lost_name: String
        lost_location: String
        lost_date: String
        status: statusEnum
        person: Person
    }

    input CreateLostInput{
        lost_name: String
        lost_location: String
        lost_date: String
        status: statusEnum
        person_id: Int
    }

    type Query {
        fetchAllLost: [Lost]
        fetchPage: Int
        fetchPageLost(page: Int!, pageSize: Int!): [Lost]
    }

    type Mutation {
        createLost(createLostInput: CreateLostInput): Int
    }
`
export const fetchPage = async () => {
    const result = await Lost.count();
    return result;
}

export const fetchAllLost = async () => {
    const result = await Lost.findAll({ include: ['person'] });

    return result;
}

export const fetchPageLost = async (_, { page, pageSize }) => {
    const offset = (page - 1) * pageSize;
    const result = await Lost.findAll({
      offset,
      limit: pageSize,
      order: [['lost_date', 'DESC'], ['id', 'DESC']],  // 원하는 정렬 기준
    });
    return result;
};

export const createLost = async (parent, args, context, info) => {
    const result = await Lost.create({
        lost_name: args.createLostInput.lost_name,
        lost_location: args.createLostInput.lost_location,
        lost_date: args.createLostInput.lost_date,
        status: args.createLostInput.status,
        person_id: args.createLostInput.person_id
    });

    return result.id;
}