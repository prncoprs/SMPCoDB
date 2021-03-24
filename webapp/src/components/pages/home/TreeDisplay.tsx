import React from "react";
import { CodeContext } from "../../model/CodeContext";
import Tree from "react-d3-tree";

export default function TreeDisplay() {
  const { result } = React.useContext(CodeContext);

  return (
    <div style={{ height: 500, width: 500 }}>
      {/* {JSON.stringify(result?.joinGraph)} */}
      {result && (
        <Tree
          data={result.joinGraph}
          orientation="vertical"
          pathFunc="step"
          translate={{ y: 100, x: 200 }}
        />
      )}
    </div>
  );
}
