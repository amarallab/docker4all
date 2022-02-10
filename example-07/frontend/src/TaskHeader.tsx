import React, { Component } from "react";
import {
    Button,
    LinearProgress,
    Typography
} from "@material-ui/core";
import "./TaskHeader.css";

export interface TaskHeaderProps {
    task_id: string;
    onHideTask: (task_id: string) => void
}

export interface TaskHeaderState {
    progress: number;
}

export class TaskHeader extends Component<TaskHeaderProps, TaskHeaderState> {

    private timerID?: number = undefined;

    constructor(props: TaskHeaderProps) {
        super(props);
        this.state = {
            progress: 0
        };
        this.handleOnClick = this.handleOnClick.bind(this);
    }

    componentDidMount() {
        this.timerID = window.setInterval(
            () => {
                this.update()
            },
            1000
        );
    }

    componentWillUnmount() {
        this.finishTimer();
    }

    finishTimer() {
        if (this.timerID != undefined) {
            window.clearInterval(this.timerID);
            this.timerID = undefined;
        }
    }

    update() {
        fetch(`/api/task/info/${this.props.task_id}`)
            .then(res => res.json())
            .then(
                (result) => {
                    const newValue = result.progress || 0;
                    if (newValue >= 1) {
                        this.finishTimer()
                    }
                    this.setState({
                        progress: newValue
                    });
                },
                (error) => {
                    console.log("Error: " + error);
                }
            );
    }

    handleOnClick() {
        this.props.onHideTask(this.props.task_id);
    }

    render() {
        return (
            <tr>
                <td className="TaskHeader-left">
                <Typography variant="overline">
                    {this.props.task_id}
                </Typography>
                <LinearProgress variant="determinate" value={this.state.progress * 100} />
                </td>
                <td className="TaskHeader-right">
                    <Button 
                        variant="contained"
                        type="button"
                        color="secondary"
                        size="small"
                        onClick={this.handleOnClick}
                    >
                        Hide
                    </Button>
                </td>
            </tr>
        );
    }
}