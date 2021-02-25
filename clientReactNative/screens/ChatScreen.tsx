import React, { useState, useCallback, useEffect } from 'react'
import { Button, NativeSyntheticEvent, StyleSheet, TextInput, TextInputSubmitEditingEventData } from 'react-native';
import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import { GiftedChat, IMessage } from 'react-native-gifted-chat'

export default class ChatScreen extends React.Component {
  socket = new WebSocket('ws://192.168.1.91:8765');
  state  = { messages: [], messageId:1 };

  componentDidMount(){
    var self= this
    this.socket.onmessage= function(this: WebSocket, ev: MessageEvent){
      var id= self.state.messageId+1
      self.setState({messages: GiftedChat.prepend([self.createBotMessage(ev.data)], self.state.messages)});
    };
  }

  componentWillUnmount(){
    this.socket.close()
  }

  handleSubmit(previousMessages: IMessage[]){
    this.socket.send(previousMessages[0].text)
    this.setState({messages: GiftedChat.prepend(previousMessages, this.state.messages)})
  }



  createBotMessage(message: string){
    var id= '_' + Math.random().toString(36).substr(2, 9);
    return {
      _id: id,
      text: message,
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'React Native',
        avatar: 'https://placeimg.com/140/140/any',
      },
    }
  }


  render(){
    return (
      <View style={styles.container}>
        <GiftedChat
          messages={this.state.messages}
          onSend={this.handleSubmit.bind(this)}
          alignTop={true}
          scrollToBottom={true}
          messagesContainerStyle={{overflow:'scroll'}}
          user={{
            _id: 1,
          }}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  }
});
