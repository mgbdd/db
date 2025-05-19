import axios from 'axios';

// Базовый URL API
const API_BASE_URL = 'http://localhost:8000'; // Измените на ваш URL бэкенда

// Создаем экземпляр axios с базовым URL
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Получение данных таблицы по указанному эндпоинту
export const fetchTableData = async (endpoint) => {
  try {
    const response = await api.get(endpoint);
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении данных:', error);
    throw new Error('Не удалось загрузить данные');
  }
};

// Получение детальной информации об одной записи
export const fetchItemDetails = async (endpoint, id) => {
  try {
    const response = await api.get(`${endpoint}${id}`);
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении детальной информации:', error);
    throw new Error('Не удалось загрузить детальную информацию');
  }
};

// Создание новой записи
export const createItem = async (endpoint, data) => {
  try {
    const response = await api.post(endpoint, data);
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании записи:', error);
    throw new Error('Не удалось создать запись');
  }
};

// Обновление записи
export const updateItem = async (endpoint, id, data) => {
  try {
    const response = await api.put(`${endpoint}${id}`, data);
    return response.data;
  } catch (error) {
    console.error('Ошибка при обновлении записи:', error);
    throw new Error('Не удалось обновить запись');
  }
};

// Удаление записи
export const deleteItem = async (endpoint, id) => {
  try {
    await api.delete(`${endpoint}${id}`);
    return true;
  } catch (error) {
    console.error('Ошибка при удалении записи:', error);
    throw new Error('Не удалось удалить запись');
  }
};

export default api;
