import { Lost } from "../Entity/lost.js"
import { Op } from "sequelize";

function buildWhere(filter = {}){
    const where = {};

    if (filter.lost_name) {
        where.lost_name = { [Op.like]: `%${filter.lost_name}%` };
    }
    if (filter.lost_location) {
        where.lost_location = { [Op.like]: `%${filter.lost_location}%` };
    }
    if (filter.lost_date) {
        const date = new Date(filter.lost_date);
        const startTimestamp = new Date(date.setHours(0, 0, 0, 0)).getTime(); // 00:00:00.000
        const endTimestamp = new Date(date.setHours(23, 59, 59, 999)).getTime(); // 23:59:59.999

        where.lost_date = {
            [Op.between]: [startTimestamp, endTimestamp]
        };
    }
    if (filter.status) {
        where.status = filter.status;
    }

    return where;
}

export const lostQuery = `
    type Person {
        id: Int
        input_time: String
    }

    enum statusEnum {
        found
        returned
    }

    input LostFilterInput {
        lost_name: String
        lost_location: String
        lost_date: String
        status: statusEnum
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
        fetchAllLost(filter: LostFilterInput): [Lost]
        fetchPage(filter: LostFilterInput): Int
        fetchPageLost(page: Int!, pageSize: Int!, filter: LostFilterInput): [Lost]
    }

    type Mutation {
        createLost(createLostInput: CreateLostInput): Int
    }
`

export const fetchPage = async (_, { filter }) => {
    const result = await Lost.count({
        where: buildWhere(filter)
    });
    return result;
}

export const fetchAllLost = async (_, { filter }) => {
    const result = await Lost.findAll({ 
        where: buildWhere(filter),
        include: ['person'],
        order: [['lost_date', 'DESC'], ['id', 'DESC']]
    });

    return result;
}

export const fetchPageLost = async (_, { page, pageSize, filter }) => {
    const offset = (page - 1) * pageSize;

    const result = await Lost.findAll({
      offset,
      limit: pageSize,
      where: buildWhere(filter),
      order: [['lost_date', 'DESC'], ['id', 'DESC']]
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