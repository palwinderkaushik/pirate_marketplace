const { useState, useEffect } = React;

const App = () => {
    const [items, setItems] = useState([]);
    const socket = io();

    useEffect(() => {
        const fetchItems = async () => {
            const result = await axios.get('/api/items');
            setItems(result.data);
        };

        fetchItems();

        socket.on('update', (data) => {
            fetchItems();
        });

        return () => socket.disconnect();
    }, []);

    return (
        <div>
            <h1>Marketplace Dashboard</h1>
            <ul>
                {items.map(item => (
                    <li key={item.id}>{item.name} - ${item.price}</li>
                ))}
            </ul>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));
