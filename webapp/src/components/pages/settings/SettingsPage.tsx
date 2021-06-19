import {
  Card,
  Typography,
  Form,
  Select,
  Button,
  message,
  Input,
  List,
  Spin,
} from "antd";
import React from "react";
import { BackEnd, Role, SettingsContext } from "../../model/SettingsContext";
import { useLocation } from "react-router";
import { CodeContext } from "../../model/CodeContext";

interface FormValue {
  role: Role;
  backend: BackEnd;
  datadir: string;
}

export default function SettingsPage() {
  const { role, setRole, backend, setBackend, datadir, setDatadir, loaded } =
    React.useContext(SettingsContext);

  const { deleteResultCache } = React.useContext(CodeContext);

  const formValue: FormValue = {
    role: role,
    backend: backend,
    datadir: datadir,
  };

  const settings = (
    <div>
      <Card>
        <Typography.Title level={5}>General Settings</Typography.Title>
        <Form
          initialValues={formValue}
          onValuesChange={(changed) => {
            if (changed.role) {
              setRole(changed.role);
            }
            if (changed.backend) {
              setBackend(changed.backend);
            }

            if (changed.datadir) {
              setDatadir(changed.datadir);
            }
          }}
        >
          <Form.Item
            label="Default data dir"
            name="datadir"
            help="Your table's data will be stored in this folder"
          >
            <Input />
          </Form.Item>
          <Form.Item label="Role" name="role">
            <Select>
              {["Client", "Server"].map((v, i) => (
                <Select.Option value={v} key={`role-${i}`}>
                  {v}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            label="Backend"
            name="backend"
            extra="This will only affect the c++ code generator"
          >
            <Select>
              {["Default Backend", "Postgres Backend"].map((v, i) => (
                <Select.Option value={v} key={`role-${i}`}>
                  {v}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Card>
      <Card title="Data" style={{ marginTop: 10 }}>
        <List>
          <List.Item>
            <List.Item.Meta
              title="Stored results"
              description="Your query results"
            />
            <Button
              onClick={() => {
                deleteResultCache();
                message.success("Delete cache successfully");
              }}
            >
              Delete
            </Button>
          </List.Item>
          <List.Item>
            <List.Item.Meta
              title="Download Data"
              description="Download table data from database"
            />
            <Button
              onClick={() => {
                deleteResultCache();
                message.success("Delete cache successfully");
              }}
            >
              Download data
            </Button>
          </List.Item>
        </List>
      </Card>
    </div>
  );

  return (
    <div style={{ padding: 10 }}>
      <Typography.Title level={3}>Settings</Typography.Title>
      {loaded ? settings : <Spin />}
    </div>
  );
}
