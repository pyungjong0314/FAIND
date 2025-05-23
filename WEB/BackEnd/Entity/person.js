import { DataTypes, Model } from "sequelize";
import { sequelize } from "../sequelizeInstance.js";

export class Person extends Model {}

Person.init({
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true
    },
    input_time: {
        type: DataTypes.DATE,
        allowNull: false
    }
}, {
    sequelize,
    modelName: 'Person',
    tableName: 'persons', // 실제 테이블 이름
    timestamps: false,   // createdAt, updatedAt 비활성화 (필요 시 true)
});