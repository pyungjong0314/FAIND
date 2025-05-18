import { Sequelize } from 'sequelize';

export const sequelize = new Sequelize('postgres', 'postgres', '0000', {
  host: 'localhost',
  port: 5432,
  dialect: 'postgres',
  logging: true,
});