// Área de login
var alerta = document.querySelector('#alert')
var btnEntrar = document.querySelector('#entry')
var nick = document.querySelector('#nick')

var telaLogin = document.querySelector('#login')
var telaChat = document.querySelector('#chat')

var mensagens = document.querySelector(".container")
var msgData = document.querySelector('#msg')
var btnSend = document.querySelector('#send')


function loadChat() {
  if (alerta.classList.contains('hidden1')) {
    alerta.classList.replace('hidden1', 'hidden');
  }
  
  if (telaLogin.classList.contains('hidden1')) {
    telaLogin.classList.replace('hidden1', 'hidden');
  }

  if (telaChat.classList.contains('hidden')) {
    telaChat.classList.replace('hidden', 'hidden1');
  }
}


function makeAlert(msg) {
  msgData.value = ''

  if (telaChat.classList.contains('hidden1')) {
    telaChat.classList.replace('hidden1', 'hidden');
  }
  if (telaLogin.classList.contains('hidden')) {
    telaLogin.classList.replace('hidden', 'hidden1');
  }

  alerta.innerText = msg;

  if (alerta.classList.contains('hidden')) {
  alerta.classList.replace('hidden', 'hidden1');
  }
}

// Validação inicial
btnEntrar.addEventListener('click', () => {
  if (nick.value != '') {

    // loadChat()
    joinChat() // Conectando ao websocket

  } else {
    alerta.innerText = 'Escolha um apelido';
    alerta.classList.replace('hidden', 'hidden1');
  }
})


// Removendo o alerta ao digitar no campo de apelido
nick.addEventListener('click', (e) => {
  if (alerta.classList.contains('hidden1')) {
    alerta.classList.replace('hidden1', 'hidden');
  }
})




// Área de mensagens

btnSend.addEventListener('click', () => {
  if (msgData.value != '') {

    criarMensagem()
    
    msgData.value = ''
  }
})


// Tratamento de Mensagens

function criarMensagem() {
  var sendMsg = JSON.stringify({
    type: 'msg',
    nick: nick.value,
    msg: msg.value,
    date: new Date().getHours() + ':' + new Date().getMinutes()
  })

  // mensagemSelf(sendMsg)
  // mensagemOthers(sendMsg)
  // mensagemAlert(sendMsg)
}


// Funções de recebido de mensagens

function mensagemSelf(doc) {
  var doc = JSON.parse(doc)

  var div = document.createElement('div')
  var message = document.createElement('p')
  
  div.classList.add('bubble')
  div.classList.add('bubble-alt')
  div.classList.add('green')
  
  message.append(doc['msg'])

  div.appendChild(message)
  mensagens.appendChild(div)
  mensagens.scrollTop = mensagens.scrollHeight
}


function mensagemOthers(doc) {
  var doc = JSON.parse(doc)

  var div = document.createElement('div')
  var data = document.createElement('p')
  var message = document.createElement('p')
  
  div.classList.add('bubble')
  
  data.classList.add('data')
  data.append(doc['nick'] + ' ' + doc['date'])

  message.append(doc['msg'])

  div.appendChild(data)
  div.appendChild(message)
  mensagens.appendChild(div)
  mensagens.scrollTop = mensagens.scrollHeight
}


function mensagemAlert(doc) {
  var doc = JSON.parse(doc.data)

  var div = document.createElement('div')
  var message = document.createElement('p')
  
  div.classList.add('central')
  
  message.append(doc['msg'])

  div.appendChild(message)
  mensagens.appendChild(div)
  mensagens.scrollTop = mensagens.scrollHeight
}


// WebSockets
function joinChat() {
  var host = location.host;

  if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
  } else {
    var ws_scheme = "ws://"
  }

  var ws = new WebSocket(ws_scheme + host + "/chat")

  ws.onopen = function () {
    ws.send(JSON.stringify({
      type: 'join',
      nick: nick.value
      })
    )
  }

  ws.onmessage = function(doc) {
    try {
      var recDoc = JSON.parse(doc.data)
    } catch (e) {
      return
    }

    if (recDoc['type'] == 'join') {
      if (recDoc['nick'] != nick.value) {
        mensagemAlert(doc)
      } else {
        loadChat()
      }
    }

    if (recDoc['type'] == 'info') {
      makeAlert(recDoc['msg'])
    }

    if (recDoc['type'] == 'msg') {
      if (recDoc['nick'] == nick.value) {
        mensagemSelf(doc)
      }
      else {
        mensagemOthers(doc)
      }
    }
  }

  ws.onclose = function() {
    makeAlert('Desconectado do Servidor')
  }

  ws.onerror = function() {
    location.reload();
  }
}
