import React, { useContext, useState } from 'react';
import { Button, Input, Spin, List, Collapse, Row, Col } from 'antd';
import { useRouteLoaderData } from "react-router-dom";
import { ROOT_ID } from '../utils/constants'
import { ChatContext } from '../state/providers';
const { TextArea } = Input;

const submitQuestion = (sessionId: string, text: string) => {
    return fetch(`/question?session_id=${sessionId}`, {
        method: "POST", headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({ question: text })
    })
}

type Source = {
    filename: string
    content: string
}
type Question = {
    question: string
    answer: string
    sources: Source[]
}

const displayQuestions = (questions: Question[]) => {
    return questions.map((v, i) => ({
        key: i,
        label: `Submission: ${v.question}.  Response: ${v.answer}`,
        children: <List>{v.sources.map((source, i) => <List.Item key={i}>{source.filename}: {source.content}</List.Item>)}</List>
    }))
}
const Chat: React.FC = () => {
    const uid = useRouteLoaderData(ROOT_ID) as string;
    const [text, setText] = useState("")
    const [isWaiting, setIsWaiting] = useState(false)
    const { questions, addQuestion } = useContext(ChatContext)
    const askQuestion = () => {
        setIsWaiting(true)
        return submitQuestion(uid, text)
            .then(result => result.json())
            .then(result => addQuestion({ ...result, question: text }))
            .finally(() => {
                setIsWaiting(false)
                setText("")
            })
    }
    const collapseItems = displayQuestions(questions)
    return <>{isWaiting ? <Spin /> : <Row>
        <Col span={24}>
            <TextArea
                value={text}
                onChange={v => setText(v.target.value)}
                rows={4}
                placeholder="Put in a question about Regions financials"
                onPressEnter={askQuestion}
            />
            <Button type="primary" onClick={askQuestion}>Ask!</Button>
        </Col>
    </Row>}
        <Row>
            <Col span={24}>
                <Collapse items={collapseItems} />
            </Col>
        </Row>

    </>
}

export default Chat;