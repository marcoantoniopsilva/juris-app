const Index = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Assessor Jurídico</h1>
        <p className="text-xl text-gray-600">Sistema de geração de minutas</p>
        <div className="mt-8">
          <a href="/login" className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700">
            Fazer Login
          </a>
        </div>
      </div>
    </div>
  );
};

export default Index;