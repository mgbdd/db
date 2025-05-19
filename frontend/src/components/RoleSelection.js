import React from 'react';
import { useNavigate } from 'react-router-dom';

const RoleSelection = () => {
  const navigate = useNavigate();

  const handleRoleSelection = (role) => {
    navigate(`/tables/${role}`);
  };

  return (
    <div className="role-selection">
      <h2 className="role-title">Выберите вашу роль для доступа к системе</h2>
      <div className="role-buttons">
        <button
          className="role-button"
          onClick={() => handleRoleSelection('pharmacist')}
        >
          Фармацевт
        </button>
        <button
          className="role-button"
          onClick={() => handleRoleSelection('provizor')}
        >
          Провизор
        </button>
        <button
          className="role-button"
          onClick={() => handleRoleSelection('manager')}
        >
          Менеджер товарной группы
        </button>
      </div>
    </div>
  );
};

export default RoleSelection;
