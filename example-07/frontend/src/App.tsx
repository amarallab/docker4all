import React, { Component } from "react";
import {
    Button,
    Container,
} from "@material-ui/core";
import './App.css';
import { TaskHeader } from './TaskHeader';
import { WaitingForm } from './WaitingForm';
import { ChatPreview } from './ChatPreview';

export interface AppState {
    task_ids: string[];
}

export default class App extends Component<{}, AppState> {

    constructor(props: {}) {
        super(props);
        this.state = {
            task_ids: []
        };
        this.handleOnNewTaskGenerated = this.handleOnNewTaskGenerated.bind(this);
        this.handleOnHideTask = this.handleOnHideTask.bind(this);
        this.handleOnLoadAllTasks = this.handleOnLoadAllTasks.bind(this);
    }

    handleOnNewTaskGenerated(new_task_id: string) {
        this.setState({
            task_ids: [...this.state.task_ids, new_task_id]
        });
    }

    handleOnHideTask(task_id: string) {
        this.setState({
            task_ids: this.state.task_ids.filter((obj) => obj !== task_id)
        });
    }

    handleOnLoadAllTasks() {
        fetch("/api/task/list")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        task_ids: result.task_list.map((obj: any) => obj.task_id)
                    });
                },
                (error) => {
                    console.log("Error: " + error);
                }
            );
    }

    render() {
        return (
            <div className="App">
                <header className="App-header">
                    Welcome to <b>Docker4All</b> console
                </header>
                <main className="App-content">
                    <WaitingForm onNewTaskGenerated={this.handleOnNewTaskGenerated} />
                    <Container maxWidth="xs">
                        <table className="App-table">
                            <tbody>
                                {this.state.task_ids.map( (value, index) => {
                                    return <TaskHeader 
                                        task_id={value} key={value} 
                                        onHideTask={this.handleOnHideTask} />
                                })}
                            </tbody>
                        </table>
                        <hr />
                        <Button 
                            variant="outlined"
                            type="button"
                            color="primary"
                            onClick={this.handleOnLoadAllTasks}
                            fullWidth
                        >
                            Load all tasks
                        </Button>
                    </Container>
                    <ChatPreview />
                </main>
            </div>
        );
    }
}
