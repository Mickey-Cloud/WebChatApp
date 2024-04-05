import { useEffect, useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";
import { useNavigate } from "react-router-dom";
import { useApi } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
  const { logout } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [createdAt, setCreatedAt] = useState("");
  const [readOnly, setReadOnly] = useState(true);

  const reset = () => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
      setCreatedAt(user.created_at);
    }
  }
  
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  useEffect(reset, [user]);
  const api = useApi();

  const mutation = useMutation({
    mutationFn: () => (
      api.put(
        `/users/me`,
        {
          username,
          email
        }
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["users"]
      });
      navigate(`/profile`);
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate()
    setReadOnly(true);
  }

  const onClick = () => {
    setReadOnly(!readOnly);
    reset();
  };

  return (
    <div className="max-w-96 mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold py-2">
        User Info
      </h2>
      <form className="border rounded px-4 py-2" onSubmit={onSubmit}>
        <FormInput
          name="Username"
          type="text"
          value={username}
          readOnly={readOnly}
          setter={setUsername}
        />
        <FormInput
          name="Email"
          type="email"
          value={email}
          readOnly={readOnly}
          setter={setEmail}
        />
        <FormInput
          name="Member Since"
          type="text"
          value={new Date(createdAt).toLocaleDateString()}
          readOnly={true}
          setter={setCreatedAt}
          />
        {!readOnly &&
          <Button className="mr-8" type="submit">
            update
          </Button>
        }
        <Button type="button" onClick={onClick}>
          {readOnly ? "edit" : "cancel"}
        </Button>
      </form>
      <Button onClick={logout}>
        logout
      </Button>
    </div>
  );
}

export default Profile;