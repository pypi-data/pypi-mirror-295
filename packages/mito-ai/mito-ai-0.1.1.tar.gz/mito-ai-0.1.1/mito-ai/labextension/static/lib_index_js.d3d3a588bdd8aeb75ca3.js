"use strict";
(self["webpackChunkmito_ai"] = self["webpackChunkmito_ai"] || []).push([["lib_index_js"],{

/***/ "./lib/Extensions/AiChat/AiChatPlugin.js":
/*!***********************************************!*\
  !*** ./lib/Extensions/AiChat/AiChatPlugin.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _ChatWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./ChatWidget */ "./lib/Extensions/AiChat/ChatWidget.js");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _VariableManager_VariableManagerPlugin__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../VariableManager/VariableManagerPlugin */ "./lib/Extensions/VariableManager/VariableManagerPlugin.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../commands */ "./lib/commands.js");







/**
 * Initialization data for the mito-ai extension.
 */
const AiChatPlugin = {
    id: 'mito_ai:plugin',
    description: 'AI chat for JupyterLab',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IRenderMimeRegistry, _VariableManager_VariableManagerPlugin__WEBPACK_IMPORTED_MODULE_4__.IVariableManager],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, notebookTracker, palette, rendermime, variableManager, restorer) => {
        // Define a widget creator function,
        // then call it to make a new widget
        const newWidget = () => {
            // Create a blank content widget inside of a MainAreaWidget
            const chatWidget = (0,_ChatWidget__WEBPACK_IMPORTED_MODULE_5__.buildChatWidget)(app, notebookTracker, rendermime, variableManager);
            return chatWidget;
        };
        let widget = newWidget();
        // Add an application command
        app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_OPEN_CHAT, {
            label: 'Your friendly Python Expert chat bot',
            execute: () => {
                // In order for the widget to be accessible, the widget must be:
                // 1. Created
                // 2. Added to the widget tracker
                // 3. Attatched to the frontend 
                // Step 1: Create the widget if its not already created
                if (!widget || widget.isDisposed) {
                    widget = newWidget();
                }
                // Step 2: Add the widget to the widget tracker if 
                // its not already there
                if (!tracker.has(widget)) {
                    tracker.add(widget);
                }
                // Step 3: Attatch the widget to the app if its not 
                // already there
                if (!widget.isAttached) {
                    app.shell.add(widget, 'left', { rank: 2000 });
                }
                // Now that the widget is potentially accessible, activating the 
                // widget opens the taskpane
                app.shell.activateById(widget.id);
                // Set focus on the chat input
                const chatInput = widget.node.querySelector('.chat-input');
                chatInput === null || chatInput === void 0 ? void 0 : chatInput.focus();
            }
        });
        app.commands.addKeyBinding({
            command: _commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_OPEN_CHAT,
            keys: ['Accel E'],
            selector: 'body',
        });
        app.shell.add(widget, 'left', { rank: 2000 });
        // Add the command to the palette.
        palette.addItem({ command: _commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_OPEN_CHAT, category: 'AI Chat' });
        // Track and restore the widget state
        let tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: widget.id
        });
        if (restorer) {
            restorer.add(widget, 'mito_ai');
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (AiChatPlugin);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatHistoryManager.js":
/*!*****************************************************!*\
  !*** ./lib/Extensions/AiChat/ChatHistoryManager.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatHistoryManager: () => (/* binding */ ChatHistoryManager)
/* harmony export */ });
class ChatHistoryManager {
    constructor(initialHistory) {
        this.getLastAIMessageIndex = () => {
            const displayOptimizedChatHistory = this.getDisplayOptimizedHistory();
            const aiMessageIndexes = displayOptimizedChatHistory.map((chatEntry, index) => {
                if (chatEntry.message.role === 'assistant') {
                    return index;
                }
                return undefined;
            }).filter(index => index !== undefined);
            return aiMessageIndexes[aiMessageIndexes.length - 1];
        };
        this.getLastAIMessage = () => {
            const lastAIMessagesIndex = this.getLastAIMessageIndex();
            if (!lastAIMessagesIndex) {
                return;
            }
            const displayOptimizedChatHistory = this.getDisplayOptimizedHistory();
            return displayOptimizedChatHistory[lastAIMessagesIndex];
        };
        this.history = initialHistory || {
            aiOptimizedChatHistory: [],
            displayOptimizedChatHistory: []
        };
    }
    getHistory() {
        return { ...this.history };
    }
    getAIOptimizedHistory() {
        return this.history.aiOptimizedChatHistory;
    }
    getDisplayOptimizedHistory() {
        return this.history.displayOptimizedChatHistory;
    }
    addUserMessage(input, activeCellCode, variables) {
        const displayMessage = {
            role: 'user',
            content: `\`\`\`python
${activeCellCode}
\`\`\`

${input}`
        };
        const aiMessage = {
            role: 'user',
            content: `You have access to the following variables:

${variables === null || variables === void 0 ? void 0 : variables.map(variable => `${JSON.stringify(variable, null, 2)}\n`).join('')}
            
Code in the active code cell:

\`\`\`python
${activeCellCode}
\`\`\`

Complete the task below. Decide what variables to use and what changes you need to make to the active code cell. Only return the full new active code cell and a concise explanation of the changes you made.

Do not: 
- Use the word "I"
- Include multiple approaches in your response
- Recreate variables that already exist

Do: 
- Use the variables that you have access to
- Keep as much of the original code as possible
- Ask for more context if you need it. 

Your task: ${input}`
        };
        this.history.displayOptimizedChatHistory.push({ message: displayMessage, error: false });
        this.history.aiOptimizedChatHistory.push(aiMessage);
    }
    addAIMessageFromResponse(message, error = false) {
        if (message.content === null) {
            return;
        }
        const aiMessage = {
            role: 'assistant',
            content: message.content
        };
        this._addAIMessage(aiMessage, error);
    }
    addAIMessageFromMessageContent(message, error = false) {
        const aiMessage = {
            role: 'assistant',
            content: message
        };
        this._addAIMessage(aiMessage, error);
    }
    _addAIMessage(aiMessage, error = false) {
        this.history.displayOptimizedChatHistory.push({ message: aiMessage, error: error });
        this.history.aiOptimizedChatHistory.push(aiMessage);
    }
    addSystemMessage(message) {
        const systemMessage = {
            role: 'system',
            content: message
        };
        this.history.displayOptimizedChatHistory.push({ message: systemMessage, error: false });
        this.history.aiOptimizedChatHistory.push(systemMessage);
    }
}


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatMessage/ChatMessage.js":
/*!**********************************************************!*\
  !*** ./lib/Extensions/AiChat/ChatMessage/ChatMessage.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_classNames__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../utils/classNames */ "./lib/utils/classNames.js");
/* harmony import */ var _CodeBlock__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./CodeBlock */ "./lib/Extensions/AiChat/ChatMessage/CodeBlock.js");
/* harmony import */ var _utils_strings__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../utils/strings */ "./lib/utils/strings.js");
/* harmony import */ var _icons_ErrorIcon__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../icons/ErrorIcon */ "./lib/icons/ErrorIcon.js");





const ChatMessage = ({ message, messageIndex, error, notebookTracker, rendermime, app, isLastAiMessage, operatingSystem }) => {
    if (message.role !== 'user' && message.role !== 'assistant') {
        // Filter out other types of messages, like system messages
        return null;
    }
    const messageContentParts = (0,_utils_strings__WEBPACK_IMPORTED_MODULE_1__.splitStringWithCodeBlocks)(message);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: (0,_utils_classNames__WEBPACK_IMPORTED_MODULE_2__.classNames)("message", { "message-user": message.role === 'user' }, { 'message-assistant': message.role === 'assistant' }, { 'message-error': error }) }, messageContentParts.map(messagePart => {
        if (messagePart.startsWith('```python')) {
            // Make sure that there is actually code in the message. 
            // An empty code will look like this '```python  ```'
            // TODO: Add a test for this since its broke a few times now.
            if (messagePart.length > 14) {
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CodeBlock__WEBPACK_IMPORTED_MODULE_3__["default"], { code: messagePart, role: message.role, rendermime: rendermime, notebookTracker: notebookTracker, app: app, isLastAiMessage: isLastAiMessage, operatingSystem: operatingSystem }));
            }
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
                error && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { marginRight: '4px' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_ErrorIcon__WEBPACK_IMPORTED_MODULE_4__["default"], null)),
                messagePart));
        }
    })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ChatMessage);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatMessage/CodeBlock.js":
/*!********************************************************!*\
  !*** ./lib/Extensions/AiChat/ChatMessage/CodeBlock.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _PythonCode__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./PythonCode */ "./lib/Extensions/AiChat/ChatMessage/PythonCode.js");
/* harmony import */ var _utils_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../utils/notebook */ "./lib/utils/notebook.js");
/* harmony import */ var _utils_strings__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../utils/strings */ "./lib/utils/strings.js");
/* harmony import */ var _style_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../style/CodeMessagePart.css */ "./style/CodeMessagePart.css");





const CodeBlock = ({ code, role, rendermime, notebookTracker, app, isLastAiMessage, operatingSystem }) => {
    const notebookName = (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_2__.getNotebookName)(notebookTracker);
    const copyCodeToClipboard = () => {
        const codeWithoutMarkdown = (0,_utils_strings__WEBPACK_IMPORTED_MODULE_3__.removeMarkdownCodeFormatting)(code);
        navigator.clipboard.writeText(codeWithoutMarkdown);
    };
    if (role === 'user') {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-container' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_PythonCode__WEBPACK_IMPORTED_MODULE_4__["default"], { code: code, rendermime: rendermime })));
    }
    if (role === 'assistant') {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-container' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-toolbar' },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-location' }, notebookName),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: () => (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_2__.writeCodeToActiveCell)(notebookTracker, code, true) },
                    "Apply to cell ",
                    isLastAiMessage ? (operatingSystem === 'mac' ? 'CMD+Y' : 'CTRL+Y') : ''),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: copyCodeToClipboard }, "Copy")),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_PythonCode__WEBPACK_IMPORTED_MODULE_4__["default"], { code: code, rendermime: rendermime })));
    }
    return react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null);
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CodeBlock);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatMessage/PythonCode.js":
/*!*********************************************************!*\
  !*** ./lib/Extensions/AiChat/ChatMessage/PythonCode.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils_strings__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../utils/strings */ "./lib/utils/strings.js");
/* harmony import */ var _style_PythonCode_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../style/PythonCode.css */ "./style/PythonCode.css");




const PythonCode = ({ code, rendermime }) => {
    const [node, setNode] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const model = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.MimeModel({
            data: { ['text/markdown']: (0,_utils_strings__WEBPACK_IMPORTED_MODULE_3__.addMarkdownCodeFormatting)(code) },
        });
        const renderer = rendermime.createRenderer('text/markdown');
        renderer.renderModel(model);
        const node = renderer.node;
        setNode(node);
    }, []);
    if (node) {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-python-code', ref: (el) => el && el.appendChild(node) });
    }
    else {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'code-message-part-python-code' });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PythonCode);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatTaskpane.js":
/*!***********************************************!*\
  !*** ./lib/Extensions/AiChat/ChatTaskpane.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../style/ChatTaskpane.css */ "./style/ChatTaskpane.css");
/* harmony import */ var _utils_classNames__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../utils/classNames */ "./lib/utils/classNames.js");
/* harmony import */ var _utils_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../utils/notebook */ "./lib/utils/notebook.js");
/* harmony import */ var _ChatMessage_ChatMessage__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./ChatMessage/ChatMessage */ "./lib/Extensions/AiChat/ChatMessage/ChatMessage.js");
/* harmony import */ var _ChatHistoryManager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./ChatHistoryManager */ "./lib/Extensions/AiChat/ChatHistoryManager.js");
/* harmony import */ var _utils_handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../utils/handler */ "./lib/utils/handler.js");
/* harmony import */ var _components_LoadingDots__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../components/LoadingDots */ "./lib/components/LoadingDots.js");
/* harmony import */ var _utils_strings__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../utils/strings */ "./lib/utils/strings.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../commands */ "./lib/commands.js");
/* harmony import */ var _icons_ResetIcon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../icons/ResetIcon */ "./lib/icons/ResetIcon.js");
/* harmony import */ var _components_IconButton__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../components/IconButton */ "./lib/components/IconButton.js");












// IMPORTANT: In order to improve the development experience, we allow you dispaly a 
// cached conversation as a starting point. Before deploying the mito-ai, we must 
// set USE_DEV_AI_CONVERSATION = false
// TODO: Write a test to ensure USE_DEV_AI_CONVERSATION is false
const USE_DEV_AI_CONVERSATION = false;
const getDefaultChatHistoryManager = () => {
    if (USE_DEV_AI_CONVERSATION) {
        const messages = [
            { role: 'system', content: 'You are an expert Python programmer.' },
            { role: 'user', content: "```python x = 5\ny=10\nx+y``` update x to 10" },
            { role: 'assistant', content: "```python x = 10\ny=10\nx+y```" },
            { role: 'user', content: "```python x = 5\ny=10\nx+y``` Explain what this code does to me" },
            { role: 'assistant', content: "This code defines two variables, x and y. Variables are named buckets that store a value. ```python x = 5\ny=10``` It then adds them together ```python x+y``` Let me know if you want me to further explain any of those concepts" }
        ];
        const chatHistory = {
            aiOptimizedChatHistory: [...messages],
            displayOptimizedChatHistory: [...messages].map(message => ({ message: message, error: false }))
        };
        return new _ChatHistoryManager__WEBPACK_IMPORTED_MODULE_2__.ChatHistoryManager(chatHistory);
    }
    else {
        const chatHistoryManager = new _ChatHistoryManager__WEBPACK_IMPORTED_MODULE_2__.ChatHistoryManager();
        chatHistoryManager.addSystemMessage('You are an expert Python programmer.');
        return chatHistoryManager;
    }
};
const ChatTaskpane = ({ notebookTracker, rendermime, variableManager, app, operatingSystem }) => {
    const textareaRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [chatHistoryManager, setChatHistoryManager] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(() => getDefaultChatHistoryManager());
    const [input, setInput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [loadingAIResponse, setLoadingAIResponse] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const chatHistoryManagerRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(chatHistoryManager);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        /*
            Why we use a ref (chatHistoryManagerRef) instead of directly accessing the state (chatHistoryManager):

            The reason we use a ref here is because the function `applyLatestCode` is registered once
            when the component mounts via `app.commands.addCommand`. If we directly used `chatHistoryManager`
            in the command's execute function, it would "freeze" the state at the time of the registration
            and wouldn't update as the state changes over time.

            React's state (`useState`) is asynchronous, and the registered command won't automatically pick up the
            updated state unless the command is re-registered every time the state changes, which would require
            unregistering and re-registering the command, causing unnecessary complexity.

            By using a ref (`chatHistoryManagerRef`), we are able to keep a persistent reference to the
            latest version of `chatHistoryManager`, which is updated in this effect whenever the state
            changes. This allows us to always access the most recent state of `chatHistoryManager` in the
            `applyLatestCode` function, without needing to re-register the command or cause unnecessary re-renders.

            We still use `useState` for `chatHistoryManager` so that we can trigger a re-render of the chat
            when the state changes.
        */
        chatHistoryManagerRef.current = chatHistoryManager;
    }, [chatHistoryManager]);
    // TextAreas cannot automatically adjust their height based on the content that they contain, 
    // so instead we re-adjust the height as the content changes here. 
    const adjustHeight = () => {
        const textarea = textareaRef.current;
        if (!textarea) {
            return;
        }
        textarea.style.height = 'auto';
        // The height should be 20 at minimum to support the placeholder
        const height = textarea.scrollHeight < 20 ? 20 : textarea.scrollHeight;
        textarea.style.height = `${height}px`;
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        adjustHeight();
    }, [input]);
    /*
        Send a message with a specific input, clearing what is currently in the chat input.
        This is useful when we want to send the error message from the MIME renderer directly
        to the AI chat.
    */
    const sendMessageWithInput = async (input) => {
        _sendMessage(input);
    };
    /*
        Send a message with the text currently in the chat input.
    */
    const sendMessageFromChat = async () => {
        _sendMessage(input);
    };
    const _sendMessage = async (input) => {
        const variables = variableManager.variables;
        const activeCellCode = (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_3__.getActiveCellCode)(notebookTracker);
        // Create a new chat history manager so we can trigger a re-render of the chat
        const updatedManager = new _ChatHistoryManager__WEBPACK_IMPORTED_MODULE_2__.ChatHistoryManager(chatHistoryManager.getHistory());
        updatedManager.addUserMessage(input, activeCellCode, variables);
        setInput('');
        setLoadingAIResponse(true);
        try {
            const apiResponse = await (0,_utils_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('mito_ai/completion', {
                method: 'POST',
                body: JSON.stringify({
                    messages: updatedManager.getAIOptimizedHistory()
                })
            });
            if (apiResponse.type === 'success') {
                const response = apiResponse.response;
                const aiMessage = response.choices[0].message;
                updatedManager.addAIMessageFromResponse(aiMessage);
                setChatHistoryManager(updatedManager);
            }
            else {
                updatedManager.addAIMessageFromMessageContent(apiResponse.errorMessage, true);
                setChatHistoryManager(updatedManager);
            }
            setLoadingAIResponse(false);
        }
        catch (error) {
            console.error('Error calling OpenAI API:', error);
        }
    };
    const displayOptimizedChatHistory = chatHistoryManager.getDisplayOptimizedHistory();
    const applyLatestCode = () => {
        const latestChatHistoryManager = chatHistoryManagerRef.current;
        const lastAIMessage = latestChatHistoryManager.getLastAIMessage();
        if (!lastAIMessage) {
            return;
        }
        const code = (0,_utils_strings__WEBPACK_IMPORTED_MODULE_5__.getCodeBlockFromMessage)(lastAIMessage.message);
        (0,_utils_notebook__WEBPACK_IMPORTED_MODULE_3__.writeCodeToActiveCell)(notebookTracker, code, true);
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        /*
            Add a new command to the JupyterLab command registry that applies the latest AI generated code
            to the active code cell. Do this inside of the useEffect so that we only register the command
            the first time we create the chat. Registering the command when it is already created causes
            errors.
        */
        app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_APPLY_LATEST_CODE, {
            execute: () => {
                applyLatestCode();
            }
        });
        app.commands.addKeyBinding({
            command: _commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_APPLY_LATEST_CODE,
            keys: ['Accel Y'],
            selector: 'body',
        });
        /*
            Add a new command to the JupyterLab command registry that sends the current chat message.
            We use this to automatically send the message when the user adds an error to the chat.
        */
        app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_SEND_MESSAGE, {
            execute: (args) => {
                if (args === null || args === void 0 ? void 0 : args.input) {
                    sendMessageWithInput(args.input.toString());
                }
            }
        });
    }, []);
    const lastAIMessagesIndex = chatHistoryManager.getLastAIMessageIndex();
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-taskpane" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-taskpane-header" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "chat-taskpane-header-title" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_IconButton__WEBPACK_IMPORTED_MODULE_7__["default"], { icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_ResetIcon__WEBPACK_IMPORTED_MODULE_8__["default"], null), title: "Clear the chat history", onClick: () => {
                    setChatHistoryManager(getDefaultChatHistoryManager());
                } })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-messages" }, displayOptimizedChatHistory.map((displayOptimizedChat, index) => {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ChatMessage_ChatMessage__WEBPACK_IMPORTED_MODULE_9__["default"], { message: displayOptimizedChat.message, error: displayOptimizedChat.error || false, messageIndex: index, notebookTracker: notebookTracker, rendermime: rendermime, app: app, isLastAiMessage: index === lastAIMessagesIndex, operatingSystem: operatingSystem }));
        }).filter(message => message !== null)),
        loadingAIResponse &&
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-loading-message" },
                "Loading AI Response ",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_LoadingDots__WEBPACK_IMPORTED_MODULE_10__["default"], null)),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("textarea", { ref: textareaRef, className: (0,_utils_classNames__WEBPACK_IMPORTED_MODULE_11__.classNames)("message", "message-user", 'chat-input'), placeholder: displayOptimizedChatHistory.length < 2 ? "Ask your personal Python expert anything!" : "Follow up on the conversation", value: input, onChange: (e) => { setInput(e.target.value); }, onKeyDown: (e) => {
                // Enter key sends the message, but we still want to allow 
                // shift + enter to add a new line.
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessageFromChat();
                }
            } })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ChatTaskpane);


/***/ }),

/***/ "./lib/Extensions/AiChat/ChatWidget.js":
/*!*********************************************!*\
  !*** ./lib/Extensions/AiChat/ChatWidget.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   buildChatWidget: () => (/* binding */ buildChatWidget),
/* harmony export */   chatIcon: () => (/* binding */ chatIcon)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _ChatTaskpane__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./ChatTaskpane */ "./lib/Extensions/AiChat/ChatTaskpane.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _src_icons_ChatIcon_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../src/icons/ChatIcon.svg */ "./src/icons/ChatIcon.svg");
/* harmony import */ var _utils_user__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../utils/user */ "./lib/utils/user.js");






const chatIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon({
    name: 'mito_ai',
    svgstr: _src_icons_ChatIcon_svg__WEBPACK_IMPORTED_MODULE_3__
});
function buildChatWidget(app, notebookTracker, rendermime, variableManager) {
    // Get the operating system here so we don't have to do it each time the chat changes.
    // The operating system won't change, duh. 
    const operatingSystem = (0,_utils_user__WEBPACK_IMPORTED_MODULE_4__.getOperatingSystem)();
    const chatWidget = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ChatTaskpane__WEBPACK_IMPORTED_MODULE_5__["default"], { app: app, notebookTracker: notebookTracker, rendermime: rendermime, variableManager: variableManager, operatingSystem: operatingSystem }));
    chatWidget.id = 'mito_ai';
    chatWidget.title.icon = chatIcon;
    chatWidget.title.caption = 'AI Chat for your JupyterLab';
    return chatWidget;
}


/***/ }),

/***/ "./lib/Extensions/ErrorMimeRenderer/ErrorMimeRendererPlugin.js":
/*!*********************************************************************!*\
  !*** ./lib/Extensions/ErrorMimeRenderer/ErrorMimeRendererPlugin.js ***!
  \*********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../commands */ "./lib/commands.js");
/* harmony import */ var _icons_MagicWand__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../icons/MagicWand */ "./lib/icons/MagicWand.js");
/* harmony import */ var _style_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../style/ErrorMimeRendererPlugin.css */ "./style/ErrorMimeRendererPlugin.css");







const ErrorMessage = ({ onDebugClick }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "error-mime-renderer-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: onDebugClick, className: 'error-mime-renderer-button' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_MagicWand__WEBPACK_IMPORTED_MODULE_5__["default"], null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Fix Error in AI Chat"))));
};
/**
 * A mime renderer plugin for the mimetype application/vnd.jupyter.stderr
 *
 * This plugin augments the standard error output with a prompt to debug the error in the chat interface.
*/
const ErrorMimeRendererPlugin = {
    id: 'jupyterlab-debug-prompt',
    autoStart: true,
    requires: [_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IRenderMimeRegistry],
    activate: (app, rendermime) => {
        const factory = rendermime.getFactory('application/vnd.jupyter.stderr');
        if (factory) {
            rendermime.addFactory({
                safe: true,
                mimeTypes: ['application/vnd.jupyter.stderr'],
                createRenderer: (options) => {
                    const originalRenderer = factory.createRenderer(options);
                    return new AugmentedStderrRenderer(app, originalRenderer);
                }
            }, -1); // Giving this renderer a lower rank than the default renderer gives this default priority
        }
    }
};
/**
 * A widget that extends the default StderrRenderer.
*/
class AugmentedStderrRenderer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor(app, originalRenderer) {
        super();
        this.app = app;
        this.originalRenderer = originalRenderer;
    }
    /**
     * Render the original error message and append the custom prompt.
     */
    async renderModel(model) {
        const resolveInChatDiv = document.createElement('div');
        react_dom__WEBPACK_IMPORTED_MODULE_1___default().render(react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ErrorMessage, { onDebugClick: () => this.openChatInterfaceWithError(model) }), resolveInChatDiv);
        this.node.appendChild(resolveInChatDiv);
        // Get the original renderer and append it to the output
        await this.originalRenderer.renderModel(model);
        this.node.appendChild(this.originalRenderer.node);
    }
    /*
        Open the chat interface and preload the error message into
        the user input.
    */
    openChatInterfaceWithError(model) {
        const conciseErrorMessage = this.getErrorString(model);
        this.app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_OPEN_CHAT);
        this.app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_6__.COMMAND_MITO_AI_SEND_MESSAGE, { input: conciseErrorMessage });
    }
    /*
        Get the error string from the model.
    */
    getErrorString(model) {
        const error = model.data['application/vnd.jupyter.error'];
        if (error && typeof error === 'object' && 'ename' in error && 'evalue' in error) {
            return `${error.ename}: ${error.evalue}`;
        }
        return '';
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ErrorMimeRendererPlugin);


/***/ }),

/***/ "./lib/Extensions/VariableManager/VariableInspector.js":
/*!*************************************************************!*\
  !*** ./lib/Extensions/VariableManager/VariableInspector.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   setupKernelListener: () => (/* binding */ setupKernelListener)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);

// TODO: Use something like raw-loader to load an actual python file 
// to make it easier to modify the script without creating syntax errors.
const pythonVariableInspectionScript = `import json


# We need to check if pandas is imported so we know if its safe
# to check for pandas dataframes 
_is_pandas_imported = False
try:
    import pandas as pd
    _is_pandas_imported = True
except:
    pass

# Function to convert dataframe to structured format
def get_dataframe_structure(df, sample_size=5):
    structure = {}
    for column in df.columns:
        structure[column] = {
            "dtype": str(df[column].dtype),
            "samples": df[column].head(sample_size).tolist()
        }
    return structure

def structured_globals():
    output = []
    for k, v in globals().items():
        if not k.startswith("_") and k not in ("In", "Out", "json") and not callable(v):
            if _is_pandas_imported and isinstance(v, pd.DataFrame):
                output.append({
                    "variable_name": k,
                    "type": "pd.DataFrame",
                    "value": get_dataframe_structure(v)
                })
            else:
                output.append({
                    "variable_name": k,
                    "type": str(type(v)),
                    "value": repr(v)
                })

    return json.dumps(output)

print(structured_globals())
`;
// Function to fetch variables and sync with the frontend
async function fetchVariablesAndUpdateState(notebookPanel, setVariables) {
    var _a;
    const kernel = (_a = notebookPanel.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
    if (kernel) {
        // Request the kernel to execute a command to fetch global variables
        const future = kernel.requestExecute({
            code: pythonVariableInspectionScript,
            // Adding silent: true prevents a execute_input message from being sent. This is important 
            // because it prevents an infinite loop where we fetch variables and in the process trigger 
            // a new execute_input which leads to fetching variables again.
            silent: true
        });
        // Listen for the output from the kernel
        future.onIOPub = (msg) => {
            // A 'stream' message represents standard output (stdout) or standard error (stderr) produced 
            // during the execution of code in the kernel.
            if (_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.isStreamMsg(msg)) {
                if (msg.content.name === 'stdout') {
                    try {
                        setVariables(JSON.parse(msg.content.text));
                    }
                    catch (e) {
                        console.log("Error parsing variables", e);
                    }
                }
            }
        };
    }
}
// Setup kernel execution listener
function setupKernelListener(notebookTracker, setVariables) {
    notebookTracker.currentChanged.connect((tracker, notebookPanel) => {
        if (!notebookPanel) {
            return;
        }
        // Listen to kernel messages
        notebookPanel.context.sessionContext.iopubMessage.connect((sender, msg) => {
            // Watch for execute_input messages, which indicate is a request to execute code. 
            // Previosuly, we watched for 'execute_result' messages, but these are only returned
            // from the kernel when a code cell prints a value to the output cell, which is not what we want.
            // TODO: Check if there is a race condition where we might end up fetching variables before the 
            // code is executed. I don't think this is the case because the kernel runs in one thread I believe.
            if (msg.header.msg_type === 'execute_input') {
                fetchVariablesAndUpdateState(notebookPanel, setVariables);
            }
        });
    });
}


/***/ }),

/***/ "./lib/Extensions/VariableManager/VariableManagerPlugin.js":
/*!*****************************************************************!*\
  !*** ./lib/Extensions/VariableManager/VariableManagerPlugin.js ***!
  \*****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IVariableManager: () => (/* binding */ IVariableManager),
/* harmony export */   VariableManager: () => (/* binding */ VariableManager),
/* harmony export */   VariableManagerPlugin: () => (/* binding */ VariableManagerPlugin),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _VariableInspector__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./VariableInspector */ "./lib/Extensions/VariableManager/VariableInspector.js");



// The provides field in JupyterLab’s JupyterFrontEndPlugin expects a token 
// that can be used to look up the service in the dependency injection system,
// so we define a new token for the VariableManager
// TODO: Should this still be called mito-ai or something else? Do I need a new name for 
// each extension? I don't think so.
const IVariableManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('mito-ai:IVariableManager');
class VariableManager {
    constructor(notebookTracker) {
        this._variables = [];
        (0,_VariableInspector__WEBPACK_IMPORTED_MODULE_2__.setupKernelListener)(notebookTracker, this.setVariables.bind(this));
    }
    get variables() {
        return this._variables;
    }
    setVariables(newVars) {
        this._variables = newVars;
        console.log("Variables updated", this._variables);
    }
}
const VariableManagerPlugin = {
    id: 'mito-ai:variable-manager',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    provides: IVariableManager,
    activate: (app, notebookTracker) => {
        return new VariableManager(notebookTracker);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (VariableManagerPlugin);


/***/ }),

/***/ "./lib/commands.js":
/*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   COMMAND_MITO_AI_APPLY_LATEST_CODE: () => (/* binding */ COMMAND_MITO_AI_APPLY_LATEST_CODE),
/* harmony export */   COMMAND_MITO_AI_OPEN_CHAT: () => (/* binding */ COMMAND_MITO_AI_OPEN_CHAT),
/* harmony export */   COMMAND_MITO_AI_SEND_MESSAGE: () => (/* binding */ COMMAND_MITO_AI_SEND_MESSAGE)
/* harmony export */ });
const MITO_AI = 'mito_ai';
const COMMAND_MITO_AI_OPEN_CHAT = `${MITO_AI}:open-chat`;
const COMMAND_MITO_AI_APPLY_LATEST_CODE = `${MITO_AI}:apply-latest-code`;
const COMMAND_MITO_AI_SEND_MESSAGE = `${MITO_AI}:send-message`;


/***/ }),

/***/ "./lib/components/IconButton.js":
/*!**************************************!*\
  !*** ./lib/components/IconButton.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_IconButton_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/IconButton.css */ "./style/IconButton.css");


const IconButton = ({ icon, onClick, title }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "icon-button", onClick: onClick, title: title }, icon));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (IconButton);


/***/ }),

/***/ "./lib/components/LoadingDots.js":
/*!***************************************!*\
  !*** ./lib/components/LoadingDots.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Mito

/*
    Dot, dot, dots. They count, so that you can display something as loading.
*/
const LoadingDots = () => {
    // We use a count to track the number of ...s to display.
    // 0 -> '', 1 -> '.', 2 -> '..', 3 -> '...'. Wraps % 4.
    const [indicatorState, setIndicatorState] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(1);
    // Schedule a change to update the loading indicator, every .5 seconds
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const interval = setInterval(() => {
            setIndicatorState(indicatorState => indicatorState + 1);
        }, 500);
        return () => clearInterval(interval);
    }, []);
    const someNumberOfDots = '.'.repeat(indicatorState % 4);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null, someNumberOfDots));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (LoadingDots);


/***/ }),

/***/ "./lib/icons/ErrorIcon.js":
/*!********************************!*\
  !*** ./lib/icons/ErrorIcon.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const ErrorIcon = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { width: "12", height: "12", viewBox: "0 0 12 12", fill: "none", xmlns: "http://www.w3.org/2000/svg" },
    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M6.00024 12C9.31251 12 12 9.31179 12 6.00024C12 2.68797 9.31803 0 6.00024 0C2.68185 0 0 2.68821 0 6.00024C0 9.31251 2.68821 12 5.99976 12H6.00024ZM5.02816 2.53827C5.02816 2.37043 5.15995 2.23809 5.32834 2.23809H6.67209C6.83993 2.23809 6.97227 2.36988 6.97227 2.53827V6.54043C6.97227 6.70827 6.84048 6.84061 6.67209 6.84061H5.32834C5.16051 6.84061 5.02816 6.70882 5.02816 6.54043V2.53827ZM6.00024 7.81209C6.53416 7.81209 6.97232 8.25026 6.97232 8.78416C6.97232 9.31807 6.53415 9.75624 6.00024 9.75624C5.46633 9.75624 5.02816 9.31807 5.02816 8.78416C5.02816 8.25026 5.46633 7.81209 6.00024 7.81209Z", fill: "black" })));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ErrorIcon);


/***/ }),

/***/ "./lib/icons/MagicWand.js":
/*!********************************!*\
  !*** ./lib/icons/MagicWand.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const MagicWandIcon = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { width: "16", height: "16", viewBox: "0 0 16 16", fill: "none", xmlns: "http://www.w3.org/2000/svg" },
    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("g", { "clip-path": "url(#clip0_8258_341)" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M11.5174 4.48082C11.2454 4.20952 10.8057 4.20952 10.5338 4.48082L7.58203 7.43256L8.56567 8.4162L11.5166 5.46446C11.788 5.19389 11.7886 4.7528 11.5173 4.48082H11.5174Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M0.20398 15.7957C0.475953 16.0677 0.915647 16.0677 1.18762 15.7957L8.07455 8.90942L7.09091 7.92578L0.20398 14.812C-0.0679933 15.084 -0.0679933 15.5237 0.20398 15.7957Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M11.1299 1.39133L10.7821 0L10.4343 1.39133L9.04297 1.73915L10.4343 2.08701L10.7821 3.47835L11.1299 2.08701L12.5213 1.73915L11.1299 1.39133Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M14.2607 3.47656L13.9128 4.8679L12.5215 5.21571L13.9128 5.56352L14.2607 6.95486L14.6085 5.56352L15.9998 5.21571L14.6085 4.8679L14.2607 3.47656Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M12.5213 7.65234L11.8256 10.435L9.04297 11.1306L11.8256 11.8263L12.5213 14.609L13.2169 11.8263L15.9996 11.1306L13.2169 10.435L12.5213 7.65234Z", fill: "white" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { d: "M6.26186 4.17397L9.04453 3.47835L6.26186 2.78267L5.56618 0L4.87056 2.78267L2.08789 3.47835L4.87056 4.17397L5.56618 6.95664L6.26186 4.17397Z", fill: "white" })),
    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("defs", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("clipPath", { id: "clip0_8258_341" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("rect", { width: "16", height: "16", fill: "white" })))));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MagicWandIcon);


/***/ }),

/***/ "./lib/icons/ResetIcon.js":
/*!********************************!*\
  !*** ./lib/icons/ResetIcon.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const ResetIcon = () => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { width: "16", height: "16", viewBox: "0 0 16 16", fill: "none", xmlns: "http://www.w3.org/2000/svg" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { "fill-rule": "evenodd", "clip-rule": "evenodd", d: "M3.83835 4.66666C4.80966 3.455 6.29889 2.6764 7.97035 2.6668C7.99332 2.66664 8.01619 2.66664 8.0391 2.6668C9.4619 2.67654 10.7524 3.24336 11.7031 4.16C11.7583 4.21317 11.8123 4.26755 11.8652 4.32312C12.7592 5.26218 13.3145 6.52685 13.3346 7.92098C13.3355 7.97619 13.3355 8.0314 13.3346 8.08666C13.3126 9.46933 12.7643 10.7241 11.8815 11.6597C11.811 11.7345 11.7383 11.8072 11.6634 11.8779C10.7263 12.763 9.46861 13.3122 8.08288 13.3327C8.03173 13.3335 7.98048 13.3335 7.92924 13.3329C5.2419 13.2969 3.0343 11.2734 2.70977 8.66526C2.6643 8.29995 2.37018 7.99995 2.00201 7.99995C1.63384 7.99995 1.3319 8.29917 1.36862 8.66547C1.39118 8.89026 1.42508 9.11313 1.47003 9.33329C1.70634 10.4909 2.24795 11.5734 3.04976 12.463C4.15336 13.6876 5.6715 14.46 7.3111 14.6306C8.9507 14.8015 10.5954 14.3588 11.9278 13.3881C13.2602 12.4173 14.1856 10.9874 14.5255 9.37434C14.8653 7.76127 14.5955 6.07954 13.768 4.65367C12.9406 3.22794 11.6143 2.15914 10.0452 1.65394C8.47618 1.14867 6.77538 1.24274 5.27151 1.91795C4.23416 2.38369 3.34124 3.10317 2.66871 3.99982V2.66649C2.66871 2.29831 2.37022 1.99982 2.00204 1.99982C1.63387 1.99982 1.33538 2.29831 1.33538 2.66649V5.99982H4.66871C5.03688 5.99982 5.33538 5.70133 5.33538 5.33315C5.33538 4.96498 5.03688 4.66649 4.66871 4.66649L3.83835 4.66666Z", fill: "black" })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ResetIcon);


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Extensions_AiChat_AiChatPlugin__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Extensions/AiChat/AiChatPlugin */ "./lib/Extensions/AiChat/AiChatPlugin.js");
/* harmony import */ var _Extensions_VariableManager_VariableManagerPlugin__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Extensions/VariableManager/VariableManagerPlugin */ "./lib/Extensions/VariableManager/VariableManagerPlugin.js");
/* harmony import */ var _Extensions_ErrorMimeRenderer_ErrorMimeRendererPlugin__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Extensions/ErrorMimeRenderer/ErrorMimeRendererPlugin */ "./lib/Extensions/ErrorMimeRenderer/ErrorMimeRendererPlugin.js");



// This is the main entry point to the mito-ai extension. It must export all of the top level 
// extensions that we want to load.
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([_Extensions_AiChat_AiChatPlugin__WEBPACK_IMPORTED_MODULE_0__["default"], _Extensions_ErrorMimeRenderer_ErrorMimeRendererPlugin__WEBPACK_IMPORTED_MODULE_1__["default"], _Extensions_VariableManager_VariableManagerPlugin__WEBPACK_IMPORTED_MODULE_2__["default"]]);


/***/ }),

/***/ "./lib/utils/classNames.js":
/*!*********************************!*\
  !*** ./lib/utils/classNames.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   classNames: () => (/* binding */ classNames)
/* harmony export */ });
/*
    A utility for constructing a valid classnames string, you can either pass
    a string, or an object that maps a string to a boolean value, indicating if
    it should be included in the final object.

    For example:
        classNames('abc', '123') = 'abc 123'
        classNames('abc', {'123': true}) = 'abc 123'
        classNames('abc', {'123': false}) = 'abc'
*/
const classNames = (...args) => {
    let finalString = '';
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        // Skip undefined arguments
        if (arg === undefined) {
            continue;
        }
        if (typeof arg === 'string') {
            finalString += arg + ' ';
        }
        else {
            Object.entries(arg).map(([className, include]) => {
                if (include) {
                    finalString += className + ' ';
                }
            });
        }
    }
    return finalString;
};


/***/ }),

/***/ "./lib/utils/handler.js":
/*!******************************!*\
  !*** ./lib/utils/handler.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Get the server settings
    const serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    // Construct the full URL
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(serverSettings.baseUrl, endPoint);
    // Add default headers
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };
    // Merge default headers with any provided headers
    init.headers = {
        ...defaultHeaders,
        ...init.headers,
    };
    // Make the request
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, serverSettings);
    }
    catch (error) {
        console.error('Error connecting to the mito_ai server:', error);
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    if (response.status === 401) {
        // This 401 error is set by the OpenAICompletionHandler class in the mito-ai python package.
        return {
            type: 'error',
            errorMessage: "You're missing the OPENAI_API_KEY environment variable. Run the following code in your terminal to set the environment variable and then relaunch the jupyter server ```python\nexport OPENAI_API_KEY=<your-api-key>\n```",
        };
    }
    if (response.status === 404) {
        // This 404 error is set by Jupyter when sending a request to the mito-ai endpoint that does not exist.
        return {
            type: 'error',
            errorMessage: "The Mito AI server is not enabled. You can enable it by running ```python\n!jupyter server extension enable mito-ai\n```",
        };
    }
    if (response.status === 500) {
        // This 500 error is set by the OpenAICompletionHandler class in the mito-ai python package. It is a 
        // generic error that is set when we haven't handled the error specifically.
        return {
            type: 'error',
            errorMessage: "There was an error communicating with OpenAI. This might be due to an incorrect API key, a temporary OpenAI outage, or a problem with your internet connection. Please try again.",
        };
    }
    // Handle the response
    let data = await response.text();
    try {
        data = JSON.parse(data);
        return {
            type: 'success',
            response: data
        };
    }
    catch (error) {
        console.error('Not a JSON response body.', response);
        return {
            type: 'error',
            errorMessage: "An error occurred while calling the Mito AI server",
        };
    }
}


/***/ }),

/***/ "./lib/utils/notebook.js":
/*!*******************************!*\
  !*** ./lib/utils/notebook.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getActiveCell: () => (/* binding */ getActiveCell),
/* harmony export */   getActiveCellCode: () => (/* binding */ getActiveCellCode),
/* harmony export */   getNotebookName: () => (/* binding */ getNotebookName),
/* harmony export */   writeCodeToActiveCell: () => (/* binding */ writeCodeToActiveCell)
/* harmony export */ });
/* harmony import */ var _strings__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./strings */ "./lib/utils/strings.js");

const getActiveCell = (notebookTracker) => {
    var _a;
    const notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
    const activeCell = notebook === null || notebook === void 0 ? void 0 : notebook.activeCell;
    return activeCell || undefined;
};
const getActiveCellCode = (notebookTracker) => {
    const activeCell = getActiveCell(notebookTracker);
    return activeCell === null || activeCell === void 0 ? void 0 : activeCell.model.sharedModel.source;
};
/*
    Writes code to the active cell in the notebook. If the code is undefined, it does nothing.
*/
const writeCodeToActiveCell = (notebookTracker, code, focus) => {
    if (code === undefined) {
        return;
    }
    const codeMirrorValidCode = (0,_strings__WEBPACK_IMPORTED_MODULE_0__.removeMarkdownCodeFormatting)(code);
    const activeCell = getActiveCell(notebookTracker);
    if (activeCell !== undefined) {
        activeCell.model.sharedModel.source = codeMirrorValidCode;
        if (focus) {
            activeCell.node.focus();
        }
    }
};
const getNotebookName = (notebookTracker) => {
    var _a;
    const notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
    return (notebook === null || notebook === void 0 ? void 0 : notebook.title.label) || 'Untitled';
};


/***/ }),

/***/ "./lib/utils/strings.js":
/*!******************************!*\
  !*** ./lib/utils/strings.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   addMarkdownCodeFormatting: () => (/* binding */ addMarkdownCodeFormatting),
/* harmony export */   getCodeBlockFromMessage: () => (/* binding */ getCodeBlockFromMessage),
/* harmony export */   removeMarkdownCodeFormatting: () => (/* binding */ removeMarkdownCodeFormatting),
/* harmony export */   splitStringWithCodeBlocks: () => (/* binding */ splitStringWithCodeBlocks)
/* harmony export */ });
/*
    Given a message from the OpenAI API, returns the content as a string.
    If the content is not a string, returns undefined.
*/
const getContentStringFromMessage = (message) => {
    // TODO: We can't assume this is a string. We need to handle the other
    // return options
    if (message.role === 'user' || message.role === 'assistant') {
        return message.content;
    }
    return undefined;
};
/*
    Given a string like "Hello ```python print('Hello, world!')```",
    returns ["Hello", "```python print('Hello, world!')```"]

    This is useful for taking an AI generated message and displaying the code in
    code blocks and the rest of the message in plain text.
*/
const splitStringWithCodeBlocks = (message) => {
    const messageContent = getContentStringFromMessage(message);
    if (!messageContent) {
        return [];
    }
    const parts = messageContent.split(/(```[\s\S]*?```)/);
    // Remove empty strings caused by consecutive delimiters, if any
    return parts.filter(part => part.trim() !== "");
};
/*
    Given a string like "Hello ```python print('Hello, world!')```",
    returns "```python print('Hello, world!')```"
*/
const getCodeBlockFromMessage = (message) => {
    const parts = splitStringWithCodeBlocks(message);
    return parts.find(part => part.startsWith('```'));
};
/*
    To display code in markdown, we need to take input values like this:

    ```python x + 1```

    And turn them into this:

    ```python
    x + 1
    ```
*/
const addMarkdownCodeFormatting = (code) => {
    const codeWithoutBackticks = code.split('```python')[1].split('```')[0].trim();
    // Note: We add a space after the code because for some unknown reason, the markdown 
    // renderer is cutting off the last character in the code block.
    return "```python\n" + codeWithoutBackticks + " " + "\n```";
};
/*
    To write code in a Jupyter Code Cell, we need to take inputs like this:

    ```python
    x + 1
    ```

    And turn them into this:

    x + 1

    Jupyter does not need the backticks.
*/
const removeMarkdownCodeFormatting = (code) => {
    return code.split('```python')[1].split('```')[0].trim();
};


/***/ }),

/***/ "./lib/utils/user.js":
/*!***************************!*\
  !*** ./lib/utils/user.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getOperatingSystem: () => (/* binding */ getOperatingSystem)
/* harmony export */ });
const getOperatingSystem = () => {
    if (navigator.userAgent.includes('Macintosh')) {
        return 'mac';
    }
    else {
        return 'windows';
    }
};


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/ChatTaskpane.css":
/*!**********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/ChatTaskpane.css ***!
  \**********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.chat-taskpane {
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: var(--chat-background-color) !important;
    --jp-sidebar-min-width: 350px;
    width: 100%;
    box-sizing: border-box;
    overflow-y: scroll;

    /* 
        Don't set padding on top from the taskpane so we can instead
        set the padding on the chat-taskpane-header instead to make 
        sure the sticky header covers all of the content behind it. 
    */
    padding-top: 0px; 
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 10px;
}

.chat-taskpane-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding-top: 10px;
    padding-bottom: 5px;
    position: sticky; /* Make the header sticky */
    top: 0; /* Stick to the top of the container */
    background-color: var(--chat-background-color); /* Ensure background color covers content behind */
    z-index: 1; /* Ensure it stays above other content */
}

.chat-taskpane-header-title {
    font-size: 14px;
    font-weight: bold;
    margin: 0;
}

.message {
    height: min-content;
    margin-bottom: 10px;
    box-sizing: border-box;
    padding: 10px;
    width: 100%;
    font-size: 14px;
}

.message-user {
    background-color: var(--chat-user-message-background-color); 
    color: var(--chat-user-message-font-color);
    border-radius: 5px;
}

.message-assistant {
    color: var(--chat-assistant-message-font-color);
}

.chat-input {
    outline: none;
    border: none;
    resize: none;
    width: 100%;
    padding: 10px;
    overflow-y: hidden;
    box-sizing: border-box;

    /* 
        The height of the chat input is set in the ChatTaskpane.tsx file. 
        See the adjustHeight function for more detail.
    */
    flex-shrink: 0 !important; 
}

.chat-loading-message {
    margin-top: 20px;
    margin-bottom: 20px;
}

.message-text {
    align-items: center;
}
`, "",{"version":3,"sources":["webpack://./style/ChatTaskpane.css"],"names":[],"mappings":"AAAA;IACI,aAAa;IACb,sBAAsB;IACtB,YAAY;IACZ,yDAAyD;IACzD,6BAA6B;IAC7B,WAAW;IACX,sBAAsB;IACtB,kBAAkB;;IAElB;;;;KAIC;IACD,gBAAgB;IAChB,kBAAkB;IAClB,mBAAmB;IACnB,oBAAoB;AACxB;;AAEA;IACI,aAAa;IACb,mBAAmB;IACnB,8BAA8B;IAC9B,mBAAmB;IACnB,iBAAiB;IACjB,mBAAmB;IACnB,gBAAgB,EAAE,2BAA2B;IAC7C,MAAM,EAAE,sCAAsC;IAC9C,8CAA8C,EAAE,kDAAkD;IAClG,UAAU,EAAE,wCAAwC;AACxD;;AAEA;IACI,eAAe;IACf,iBAAiB;IACjB,SAAS;AACb;;AAEA;IACI,mBAAmB;IACnB,mBAAmB;IACnB,sBAAsB;IACtB,aAAa;IACb,WAAW;IACX,eAAe;AACnB;;AAEA;IACI,2DAA2D;IAC3D,0CAA0C;IAC1C,kBAAkB;AACtB;;AAEA;IACI,+CAA+C;AACnD;;AAEA;IACI,aAAa;IACb,YAAY;IACZ,YAAY;IACZ,WAAW;IACX,aAAa;IACb,kBAAkB;IAClB,sBAAsB;;IAEtB;;;KAGC;IACD,yBAAyB;AAC7B;;AAEA;IACI,gBAAgB;IAChB,mBAAmB;AACvB;;AAEA;IACI,mBAAmB;AACvB","sourcesContent":[".chat-taskpane {\n    display: flex;\n    flex-direction: column;\n    height: 100%;\n    background-color: var(--chat-background-color) !important;\n    --jp-sidebar-min-width: 350px;\n    width: 100%;\n    box-sizing: border-box;\n    overflow-y: scroll;\n\n    /* \n        Don't set padding on top from the taskpane so we can instead\n        set the padding on the chat-taskpane-header instead to make \n        sure the sticky header covers all of the content behind it. \n    */\n    padding-top: 0px; \n    padding-left: 10px;\n    padding-right: 10px;\n    padding-bottom: 10px;\n}\n\n.chat-taskpane-header {\n    display: flex;\n    flex-direction: row;\n    justify-content: space-between;\n    align-items: center;\n    padding-top: 10px;\n    padding-bottom: 5px;\n    position: sticky; /* Make the header sticky */\n    top: 0; /* Stick to the top of the container */\n    background-color: var(--chat-background-color); /* Ensure background color covers content behind */\n    z-index: 1; /* Ensure it stays above other content */\n}\n\n.chat-taskpane-header-title {\n    font-size: 14px;\n    font-weight: bold;\n    margin: 0;\n}\n\n.message {\n    height: min-content;\n    margin-bottom: 10px;\n    box-sizing: border-box;\n    padding: 10px;\n    width: 100%;\n    font-size: 14px;\n}\n\n.message-user {\n    background-color: var(--chat-user-message-background-color); \n    color: var(--chat-user-message-font-color);\n    border-radius: 5px;\n}\n\n.message-assistant {\n    color: var(--chat-assistant-message-font-color);\n}\n\n.chat-input {\n    outline: none;\n    border: none;\n    resize: none;\n    width: 100%;\n    padding: 10px;\n    overflow-y: hidden;\n    box-sizing: border-box;\n\n    /* \n        The height of the chat input is set in the ChatTaskpane.tsx file. \n        See the adjustHeight function for more detail.\n    */\n    flex-shrink: 0 !important; \n}\n\n.chat-loading-message {\n    margin-top: 20px;\n    margin-bottom: 20px;\n}\n\n.message-text {\n    align-items: center;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/CodeMessagePart.css":
/*!*************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/CodeMessagePart.css ***!
  \*************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.code-message-part-container {
    display: flex;
    flex-direction: column;

    background-color: var(--chat-background-color);
    border-radius: 3px;
    border: 1px solid var(--chat-user-message-font-color);
    overflow: hidden;
}

.code-message-part-toolbar {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;

    width: 100%;
    background-color: var(--chat-user-message-background-color);
    border-bottom: 1px solid var(--chat-user-message-font-color);
    font-size: 0.8em;
}

.code-location {
    flex-grow: 1;
    margin-left: 5px;
    color: var(--chat-user-message-font-color);
}

.code-message-part-toolbar button {
    background-color: var(--chat-user-message-background-color);
    border: none;
    border-left: 1px solid var(--chat-user-message-font-color);
    border-radius: 0px;

    font-size: 0.8em;
    color: var(--chat-user-message-font-color);
}

.code-message-part-toolbar button:hover {
    background-color: var(--chat-background-color);
    color: var(--chat-assistant-message-font-color);
}`, "",{"version":3,"sources":["webpack://./style/CodeMessagePart.css"],"names":[],"mappings":"AAAA;IACI,aAAa;IACb,sBAAsB;;IAEtB,8CAA8C;IAC9C,kBAAkB;IAClB,qDAAqD;IACrD,gBAAgB;AACpB;;AAEA;IACI,aAAa;IACb,mBAAmB;IACnB,mBAAmB;IACnB,uBAAuB;;IAEvB,WAAW;IACX,2DAA2D;IAC3D,4DAA4D;IAC5D,gBAAgB;AACpB;;AAEA;IACI,YAAY;IACZ,gBAAgB;IAChB,0CAA0C;AAC9C;;AAEA;IACI,2DAA2D;IAC3D,YAAY;IACZ,0DAA0D;IAC1D,kBAAkB;;IAElB,gBAAgB;IAChB,0CAA0C;AAC9C;;AAEA;IACI,8CAA8C;IAC9C,+CAA+C;AACnD","sourcesContent":[".code-message-part-container {\n    display: flex;\n    flex-direction: column;\n\n    background-color: var(--chat-background-color);\n    border-radius: 3px;\n    border: 1px solid var(--chat-user-message-font-color);\n    overflow: hidden;\n}\n\n.code-message-part-toolbar {\n    display: flex;\n    flex-direction: row;\n    align-items: center;\n    justify-content: center;\n\n    width: 100%;\n    background-color: var(--chat-user-message-background-color);\n    border-bottom: 1px solid var(--chat-user-message-font-color);\n    font-size: 0.8em;\n}\n\n.code-location {\n    flex-grow: 1;\n    margin-left: 5px;\n    color: var(--chat-user-message-font-color);\n}\n\n.code-message-part-toolbar button {\n    background-color: var(--chat-user-message-background-color);\n    border: none;\n    border-left: 1px solid var(--chat-user-message-font-color);\n    border-radius: 0px;\n\n    font-size: 0.8em;\n    color: var(--chat-user-message-font-color);\n}\n\n.code-message-part-toolbar button:hover {\n    background-color: var(--chat-background-color);\n    color: var(--chat-assistant-message-font-color);\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/ErrorMimeRendererPlugin.css":
/*!*********************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/ErrorMimeRendererPlugin.css ***!
  \*********************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.error-mime-renderer-container {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: start;
    background-color: var(--jp-rendermime-error-background);
    width: 100%;
}

.error-mime-renderer-button {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;

    background-color: var(--jp-error-color3);
    border: var(--jp-error-color0) 1px solid;
    color: var(--jp-error-color0);

    margin: 10px;
    box-sizing: border-box;

    border-radius: 3px;
    font-size: 14px;
}

.error-mime-renderer-button svg {
    margin-right: 5px;
}

.error-mime-renderer-button p {
    margin: 0;
}

`, "",{"version":3,"sources":["webpack://./style/ErrorMimeRendererPlugin.css"],"names":[],"mappings":"AAAA;IACI,aAAa;IACb,mBAAmB;IACnB,sBAAsB;IACtB,kBAAkB;IAClB,uDAAuD;IACvD,WAAW;AACf;;AAEA;IACI,aAAa;IACb,mBAAmB;IACnB,sBAAsB;IACtB,mBAAmB;;IAEnB,wCAAwC;IACxC,wCAAwC;IACxC,6BAA6B;;IAE7B,YAAY;IACZ,sBAAsB;;IAEtB,kBAAkB;IAClB,eAAe;AACnB;;AAEA;IACI,iBAAiB;AACrB;;AAEA;IACI,SAAS;AACb","sourcesContent":[".error-mime-renderer-container {\n    display: flex;\n    flex-direction: row;\n    justify-content: start;\n    align-items: start;\n    background-color: var(--jp-rendermime-error-background);\n    width: 100%;\n}\n\n.error-mime-renderer-button {\n    display: flex;\n    flex-direction: row;\n    justify-content: start;\n    align-items: center;\n\n    background-color: var(--jp-error-color3);\n    border: var(--jp-error-color0) 1px solid;\n    color: var(--jp-error-color0);\n\n    margin: 10px;\n    box-sizing: border-box;\n\n    border-radius: 3px;\n    font-size: 14px;\n}\n\n.error-mime-renderer-button svg {\n    margin-right: 5px;\n}\n\n.error-mime-renderer-button p {\n    margin: 0;\n}\n\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/IconButton.css":
/*!********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/IconButton.css ***!
  \********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.icon-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
}`, "",{"version":3,"sources":["webpack://./style/IconButton.css"],"names":[],"mappings":"AAAA;IACI,6BAA6B;IAC7B,YAAY;IACZ,eAAe;AACnB","sourcesContent":[".icon-button {\n    background-color: transparent;\n    border: none;\n    cursor: pointer;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/PythonCode.css":
/*!********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/PythonCode.css ***!
  \********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.code-message-part-python-code pre {
    flex-grow: 1;
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 10px;
    font-size: 12px;
    font-family: Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New;
    white-space: nowrap;
    overflow-x: auto;
}

.code-message-part-python-code .jp-RenderedHTMLCommon > *:last-child {
    /* 
        Remove the default Jupyter ending margin 
        so that the rendered code is flush with the bottom
        of the CodeMessagePart
    */
    margin-bottom: 0px;
}`, "",{"version":3,"sources":["webpack://./style/PythonCode.css"],"names":[],"mappings":"AAAA;IACI,YAAY;IACZ,YAAY;IACZ,WAAW;IACX,SAAS;IACT,aAAa;IACb,eAAe;IACf,iHAAiH;IACjH,mBAAmB;IACnB,gBAAgB;AACpB;;AAEA;IACI;;;;KAIC;IACD,kBAAkB;AACtB","sourcesContent":[".code-message-part-python-code pre {\n    flex-grow: 1;\n    height: 100%;\n    width: 100%;\n    margin: 0;\n    padding: 10px;\n    font-size: 12px;\n    font-family: Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New;\n    white-space: nowrap;\n    overflow-x: auto;\n}\n\n.code-message-part-python-code .jp-RenderedHTMLCommon > *:last-child {\n    /* \n        Remove the default Jupyter ending margin \n        so that the rendered code is flush with the bottom\n        of the CodeMessagePart\n    */\n    margin-bottom: 0px;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/ChatTaskpane.css":
/*!********************************!*\
  !*** ./style/ChatTaskpane.css ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./ChatTaskpane.css */ "./node_modules/css-loader/dist/cjs.js!./style/ChatTaskpane.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_ChatTaskpane_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/CodeMessagePart.css":
/*!***********************************!*\
  !*** ./style/CodeMessagePart.css ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./CodeMessagePart.css */ "./node_modules/css-loader/dist/cjs.js!./style/CodeMessagePart.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_CodeMessagePart_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/ErrorMimeRendererPlugin.css":
/*!*******************************************!*\
  !*** ./style/ErrorMimeRendererPlugin.css ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./ErrorMimeRendererPlugin.css */ "./node_modules/css-loader/dist/cjs.js!./style/ErrorMimeRendererPlugin.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_ErrorMimeRendererPlugin_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/IconButton.css":
/*!******************************!*\
  !*** ./style/IconButton.css ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./IconButton.css */ "./node_modules/css-loader/dist/cjs.js!./style/IconButton.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_IconButton_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/PythonCode.css":
/*!******************************!*\
  !*** ./style/PythonCode.css ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./PythonCode.css */ "./node_modules/css-loader/dist/cjs.js!./style/PythonCode.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_PythonCode_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./src/icons/ChatIcon.svg":
/*!********************************!*\
  !*** ./src/icons/ChatIcon.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<svg width=\"19\" height=\"20\" viewBox=\"0 0 19 20\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n    <path d=\"M15.0626 4.8125C15.5466 4.8125 15.9376 5.20352 15.9376 5.6875C15.9376 6.17148 15.5466 6.5625 15.0626 6.5625C14.5787 6.5625 14.1876 6.17148 14.1876 5.6875C14.1876 5.20352 14.5787 4.8125 15.0626 4.8125ZM12.0001 4.8125C12.4841 4.8125 12.8751 5.20352 12.8751 5.6875C12.8751 6.17148 12.4841 6.5625 12.0001 6.5625C11.5162 6.5625 11.1251 6.17148 11.1251 5.6875C11.1251 5.20352 11.5162 4.8125 12.0001 4.8125ZM8.93764 4.8125C9.42162 4.8125 9.81264 5.20352 9.81264 5.6875C9.81264 6.17148 9.42162 6.5625 8.93764 6.5625C8.45365 6.5625 8.06264 6.17148 8.06264 5.6875C8.06264 5.20352 8.45365 4.8125 8.93764 4.8125ZM12.0001 0C15.8665 0 19.0001 2.5457 19.0001 5.6875C19.0001 6.98906 18.456 8.18125 17.5537 9.14102C17.9611 10.2184 18.8087 11.1316 18.8224 11.1426C19.0029 11.334 19.0521 11.6129 18.9482 11.8535C18.8443 12.0941 18.6064 12.25 18.3439 12.25C16.6622 12.25 15.3361 11.5473 14.5404 10.984C13.7501 11.2328 12.897 11.375 12.0001 11.375C8.13373 11.375 5.00014 8.8293 5.00014 5.6875C5.00014 2.5457 8.13373 0 12.0001 0ZM12.0001 10.0625C12.7302 10.0625 13.4521 9.95039 14.1439 9.73164L14.7646 9.53477L15.2978 9.91211C15.6888 10.1883 16.2247 10.4973 16.8701 10.7051C16.6705 10.3742 16.4763 10.0023 16.3259 9.60586L16.0361 8.8375L16.5994 8.24141C17.0943 7.71367 17.6876 6.84141 17.6876 5.6875C17.6876 3.27578 15.1365 1.3125 12.0001 1.3125C8.86381 1.3125 6.31264 3.27578 6.31264 5.6875C6.31264 8.09922 8.86381 10.0625 12.0001 10.0625Z\" fill=\"black\"/>\n    <path d=\"M7 7C3.13359 7 0 9.5457 0 12.6875C0 14.0437 0.585156 15.2852 1.55859 16.2613C1.2168 17.6395 0.0738281 18.8672 0.0601563 18.8809C0 18.9438 -0.0164062 19.0367 0.0191406 19.1188C0.0546875 19.2008 0.13125 19.25 0.21875 19.25C2.03164 19.25 3.39063 18.3805 4.06328 17.8445C4.95742 18.1809 5.95 18.375 7 18.375C10.8664 18.375 14 15.8293 14 12.6875C14 9.5457 10.8664 7 7 7ZM3.5 13.5625C3.01602 13.5625 2.625 13.1715 2.625 12.6875C2.625 12.2035 3.01602 11.8125 3.5 11.8125C3.98398 11.8125 4.375 12.2035 4.375 12.6875C4.375 13.1715 3.98398 13.5625 3.5 13.5625ZM7 13.5625C6.51602 13.5625 6.125 13.1715 6.125 12.6875C6.125 12.2035 6.51602 11.8125 7 11.8125C7.48398 11.8125 7.875 12.2035 7.875 12.6875C7.875 13.1715 7.48398 13.5625 7 13.5625ZM10.5 13.5625C10.016 13.5625 9.625 13.1715 9.625 12.6875C9.625 12.2035 10.016 11.8125 10.5 11.8125C10.984 11.8125 11.375 12.2035 11.375 12.6875C11.375 13.1715 10.984 13.5625 10.5 13.5625Z\" fill=\"black\"/>\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.d3d3a588bdd8aeb75ca3.js.map