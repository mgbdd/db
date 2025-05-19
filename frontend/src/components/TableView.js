import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchTableData } from '../services/api';

const TableView = () => {
  const { role, table } = useParams();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tableInfo, setTableInfo] = useState(null);

  useEffect(() => {
    // Определяем информацию о таблице
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
    
    const currentTable = availableTables.find(t => t.id === table);
    if (currentTable) {
      setTableInfo(currentTable);
    }
  }, [role, table]);

  useEffect(() => {
    if (tableInfo) {
      const loadData = async () => {
        try {
          setLoading(true);
          const result = await fetchTableData(tableInfo.endpoint);
          setData(result);
          setLoading(false);
        } catch (err) {
          setError(err.message);
          setLoading(false);
        }
      };
      
      loadData();
    }
  }, [tableInfo]);

  const getRoleTitle = () => {
    switch (role) {
      case 'pharmacist': return 'Фармацевт';
      case 'provizor': return 'Провизор';
      case 'manager': return 'Менеджер товарной группы';
      default: return '';
    }
  };

  const renderTableHeaders = () => {
    if (data.length === 0) return null;
    
    const item = data[0];
    return (
      <tr>
        {Object.keys(item).map((key) => (
          <th key={key}>{key}</th>
        ))}
      </tr>
    );
  };

  const renderTableRows = () => {
    if (data.length === 0) return null;
    
    return data.map((item, index) => (
      <tr key={index}>
        {Object.values(item).map((value, i) => (
          <td key={i}>
            {value === null ? '-' : 
             typeof value === 'object' ? JSON.stringify(value) : 
             String(value)}
          </td>
        ))}
      </tr>
    ));
  };

  if (!tableInfo) {
    return <div>Таблица не найдена</div>;
  }

  return (
    <div>
      <div className="breadcrumbs">
        <Link to="/">Главная</Link> / <Link to={`/tables/${role}`}>{getRoleTitle()}</Link> / <span>{tableInfo.name}</span>
      </div>
      
      <h2>{tableInfo.name}</h2>

      {loading && <p>Загрузка данных...</p>}
      {error && <p>Ошибка: {error}</p>}

      {!loading && !error && data.length > 0 && (
        <table className="data-table">
          <thead>
            {renderTableHeaders()}
          </thead>
          <tbody>
            {renderTableRows()}
          </tbody>
        </table>
      )}

      {!loading && !error && data.length === 0 && (
        <p>Нет данных для отображения</p>
      )}
    </div>
  );
};

export default TableView;
