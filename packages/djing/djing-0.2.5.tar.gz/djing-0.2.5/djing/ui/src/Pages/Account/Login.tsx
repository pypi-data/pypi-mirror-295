import { useForm } from "@inertiajs/react";
import React from "react";

const LoginPage: React.FC = () => {
  const { post, processing, data } = useForm({
    email: "",
    password: "",
  });

  const process_login = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    post("login", { data });
  };

  return (
    <div>
      <form onSubmit={process_login}>
        <div>
          <input type="email" placeholder="email" />
        </div>
        <div>
          <input type="password" placeholder="password" />
        </div>
        <div>
          <button type="submit">login</button>
        </div>
      </form>
    </div>
  );
};

export default LoginPage;
