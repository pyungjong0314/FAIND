import { Person } from "../Entity/person.js"

export const personQuery = `
    type Person {
        id: Int
        input_time: String
    }

    type Query {
        fetchPersons: [Person]
    }

    type Mutation {
        createPerson(input_time: String): Int
    }
`

export const fetchPersons = async () => {
    const result = await Person.findAll();

    return result;
}

export const createPerson = async (parent, args, context, info) => {
    const result = await Person.create({
        input_time: args.input_time
    })

    return result.id;
}