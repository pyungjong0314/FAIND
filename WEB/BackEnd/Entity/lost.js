import { DataTypes, Model } from "sequelize";
import { sequelize } from "../sequelizeInstance.js";
import { Person } from './person.js';

export class Lost extends Model {}

Lost.init({
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true
    },
    lost_name: {
        type: DataTypes.STRING,
        allowNull: false
    },
    lost_location: {
        type: DataTypes.STRING,
        allowNull: true
    },
    lost_date: {
        type: DataTypes.DATE,
        allowNull: true
    },
    status: {
        type: DataTypes.ENUM('found', 'returned'),
        allowNull: false,
        defaultValue: 'found'
    },
    person_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
          model: 'persons', // 참조할 테이블 이름 (문자열)
          key: 'id'         // 참조할 컬럼
        }
    }
}, {
    sequelize,
    modelName: 'Lost',
    tableName: 'lost', // 실제 테이블 이름
    timestamps: false,   // createdAt, updatedAt 비활성화 (필요 시 true)
});

Lost.belongsTo(Person, { foreignKey: 'person_id', as: 'person' });