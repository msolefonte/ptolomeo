const axios = require('axios');
const { KJUR } = require('jsrsasign');

module.exports = class DialogFlowBot {
    constructor(creds, sessionId) {
        this.creds = creds;
        this.sessionId = sessionId;
    }

    async generateToken() {
        const header = {
            alg: 'RS256',
            typ: 'JWT',
            kid: this.creds.private_key_id
        };

        // Payload
        const payload = {
            iss: this.creds.client_email,
            sub: this.creds.client_email,
            iat: KJUR.jws.IntDate.get('now'),
            exp: KJUR.jws.IntDate.get('now + 1hour'),
            aud: 'https://dialogflow.googleapis.com/google.cloud.dialogflow.v2.Sessions'
        };

        const stringHeader = JSON.stringify(header);
        const stringPayload = JSON.stringify(payload);
        this.token = await KJUR.jws.JWS.sign('RS256', stringHeader, stringPayload, this.creds.private_key);
    }

    async detectIntent(text, languageCode = 'es') {
        const session = 'projects/' + this.creds.project_id + '/agent/sessions/' + this.sessionId;
        axios.defaults.baseURL = 'https://dialogflow.googleapis.com';
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        axios.defaults.headers.post['Content-Type'] = 'application/json';

        // Can throw errors
        const response = await axios.post(`/v2/${session}:detectIntent`, {
                queryInput: {
                    text: {
                        text,
                        languageCode
                    }
                }
            });

        return response.data;
    }
};