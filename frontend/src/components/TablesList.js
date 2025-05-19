import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';

const TablesList = () => {
  const { role } = useParams();
  const navigate = useNavigate();
  const [tables, setTables] = useState([]);

  useEffect(() => {
    // Здесь определяем доступные таблицы в зависимости от роли
    let availableTables = [];
    switch (role) {
      case 'pharmacist':
        availableTables = [
          { id: 'clients', name: 'Клиенты', endpoint: '/clients/' },
          { id: 'orders', name: 'Заказы', endpoint: '/orders/' },
          { id: 'medicines', name: 'Лекарства', endpoint: '/medicines/' },
          { id: 'prescriptions', name: 'Рецепты', endpoint: '/prescriptions/' },
        ];
        break;
      case 'provizor':
        availableTables = [
          { id: 'medicines', name: 'Лекарства', endpoint: '/medicines/' },
          { id: 'compositions', name: 'Составы лекарств', endpoint: '/compositions/' },
          { id: 'technologies', name: 'Технологии приготовления', endpoint: '/technologies/' },
          { id: 'ingredients', name: 'Ингредиенты', endpoint: '/ingredients/' },
          { id: 'medications_critical', name: 'Критический уровень лекарств', endpoint: '/queries/medications/critical' },
          { id: 'producing_orders', name: 'Заказы в производстве', endpoint: '/queries/orders/producing' },
        ];
        break;
      case 'manager':
        availableTables = [
          { id: 'medications', name: 'Медикаменты', endpoint: '/medications/' },
          { id: 'inventories', name: 'Инвентаризация', endpoint: '/inventories/' },
          { id: 'deliveries', name: 'Поставки', endpoint: '/deliveries/' },
          { id: 'low_stock', name: 'Медикаменты на исходе', endpoint: '/queries/medications/low-stock' },
          { id: 'top_medications', name: 'Популярные медикаменты', endpoint: '/queries/medications/top' },
        ];
        break;
      default:
        break;
    }
    setTables(availableTables);
  }, [role]);

  const handleTableClick = (tableId) => {
    navigate(`/tables/${role}/${tableId}`);
  };

  const getRoleTitle = () => {
    switch (role) {
      case 'pharmacist': return 'Фармацевт';
      case 'provizor': return 'Провизор';
      case 'manager': return 'Менеджер товарной группы';
      default: return '';
    }
  };

  return (
    <div>
      <div className="breadcrumbs">
        <Link to="/">Главная</Link> / <span>{getRoleTitle()}</span>
      </div>
      <h2>Доступные таблицы для роли: {getRoleTitle()}</h2>
      <div className="tables-list">
        {tables.map((table) => (
          <div
            key={table.id}
            className="table-item"
            onClick={() => handleTableClick(table.id)}
          >
            <h3>{table.name}</h3>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TablesList;
