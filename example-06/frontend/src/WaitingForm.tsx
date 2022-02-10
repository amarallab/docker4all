import React, { Component } from 'react';
import {
    Container,
    Typography,
    TextField,
    Button,
} from "@material-ui/core";
import './WaitingForm.css';

export interface WaitingFormProps {
    onNewTaskGenerated: (new_task_id: string) => void
}

export interface WaitingFormState {
    delay?: string;
}

export class WaitingForm extends Component<WaitingFormProps, WaitingFormState> {
    
    constructor(props: WaitingFormProps) {
        super(props);
        this.state = {
            delay: undefined
        };
        this.handleOnChange = this.handleOnChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    isValid = () => {
        if (this.state.delay == undefined || this.state.delay.length == 0) {
            return false;
        }
        return !isNaN(Number(this.state.delay));
    }

    handleOnChange(ev: React.ChangeEvent<HTMLInputElement>) {
        this.setState({
            delay: ev.target.value
        });
    }

    handleSubmit() {
        console.log(this.state);
        fetch(`/api/run/waiting/${this.state.delay}`)
            .then(res => res.json())
            .then( 
                (result) => {
                    this.props.onNewTaskGenerated(result.task_id);
                },
                (error) => {
                    console.log("Error: " + error);
                }
            );
    }

    render() {
        return (
            <Container maxWidth="xs">
                <Typography variant="h4">
                    Waiting Task
                </Typography>
                <TextField
                    variant="outlined"
                    margin="normal"
                    label="Delay (in seconds)"
                    onChange={this.handleOnChange}
                    fullWidth
                    required
                />
                <Button
                    variant="contained"
                    type="submit"
                    color="primary"
                    disabled={!this.isValid()}
                    onClick={this.handleSubmit}
                    fullWidth
                    >
                        Start Task
                </Button>
            </Container>
        )
    }
}