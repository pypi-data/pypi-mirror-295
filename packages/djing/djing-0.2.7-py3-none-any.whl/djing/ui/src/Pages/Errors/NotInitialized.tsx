import React from "react";

const NotInitialized: React.FC = ({ context }: any) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-red-600 mb-4">
          {context.error_message}
        </h1>
        <p className="text-gray-700 text-lg mb-4">
          Please run the below command to continue:
        </p>
        <div className="bg-gray-100 p-4 rounded-md mb-4">
          <pre className="text-sm font-mono text-gray-800">
            <code>python manage.py init</code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export default NotInitialized;
