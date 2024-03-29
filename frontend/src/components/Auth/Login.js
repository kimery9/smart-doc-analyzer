import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import credentials from '../../credentials.json'

const OAuthLogin = ({ onSuccess, onFailure }) => {
    const { web: { client_id } } = credentials;

    return (
        <GoogleLogin
            clientId={client_id}
            onSuccess={onSuccess}
            onError={onFailure}
            // Use the render prop if you want to customize the button
            render={renderProps => (
                <button onClick={renderProps.onClick} disabled={renderProps.disabled}>
                    Login with Google
                </button>
            )}
        />
    );
};

export default OAuthLogin;