import React, { useState } from 'react';
import { Button, Input, Spin } from 'antd';
import type { CollapseProps } from 'antd';
import { Collapse } from 'antd';
const text = `
  A dog is a type of domesticated animal.
  Known for its loyalty and faithfulness,
  it can be found as a welcome guest in many households across the world.
`;

const items: CollapseProps['items'] = [
    {
        key: '1',
        label: 'This is panel header 1',
        children: <p>{text}</p>,
    },
    {
        key: '2',
        label: 'This is panel header 2',
        children: <p>{text}</p>,
    },
    {
        key: '3',
        label: 'This is panel header 3',
        children: <p>{text}</p>,
    },
];

const App: React.FC = () => {
    const onChange = (key: string | string[]) => {
        console.log(key);
    };

    return <Collapse items={items} defaultActiveKey={['1']} onChange={onChange} />;
};

export default App;


const { TextArea } = Input;

const submitQuestion = (text: string) => {
    return fetch("/question", { method: "POST", body: JSON.stringify({ question: text }) })
}

const App: React.FC = () => {
    const [text, setText] = useState("")
    const [result, setResult] = useState("")
    const [isWaiting, setIsWaiting] = useState(false)
    const [questions, setQuestions] = useState([]) //append previous questions and answers
    const askQuestion = () => {
        setIsWaiting(true)
        return submitQuestion(text).then(result => result.json()).then(setResult).finally(() => setIsWaiting(false))
    }
    return <>{isWaiting ? <Spin /> : <>
        <TextArea
            value={text}
            onChange={v => setText(v.target.value)}
            rows={4}
            placeholder="Put in a question about Regions financials"
            maxLength={6}
            onPressEnter={askQuestion}
        />
        <Button type="primary" onClick={askQuestion}>Ask!</Button>
    </>}
        <Collapse items={items} defaultActiveKey={['1']} onChange={onChange} />
    </>
}

export default App;