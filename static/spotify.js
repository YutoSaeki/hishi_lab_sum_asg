// // Spotify Web Playback SDK

// //初期化
// window.onSpotifyWebPlaybackSDKReady = () => {
//     const token = "{{ access_token }}";
//     //console.log('トークン：%s',token);//確認用
//     const player = new Spotify.Player({
//         name: 'Web Playback SDK Quick Start Player',
//         //volume: 0.5,
//         getOAuthToken: cb => { cb(token); }
//     });

//     // Ready（接続準備ができたとき）
//     player.addListener('ready', ({ device_id }) => {
//         console.log('Ready with Device ID', device_id);
//         localStorage.setItem('device_id', device_id);
//     });

//     // Not Ready（接続が切断されたとき）
//     player.addListener('not_ready', ({ device_id }) => {
//         console.log('Device ID has gone offline', device_id);
//     });

//     //SDK初期化中にエラーが起きた場合の処理
//     player.addListener('initialization_error', ({ message }) => {
//         console.error(message);
//     });
//     player.addListener('authentication_error', ({ message }) => {
//         console.error(message);
//     });
//     player.addListener('account_error', ({ message }) => {
//         console.error(message);
//     });
  

//     // Player State Changed
//     player.addListener('player_state_changed', state => {
//         if (state) {
//             const trackName = state.track_window.current_track.name;
//             document.getElementById('trackName').textContent = trackName;
//         }
//     });

//     // インスタンスの接続を実行
//     player.connect();

//     // Play button
//     document.getElementById('playButton').onclick = () => {
//         player.resume().then(() => {
//             console.log('Resumed!');
//         });
//     };

//     // Pause button
//     document.getElementById('pauseButton').onclick = () => {
//         player.pause().then(() => {
//             console.log('Paused!');
//         });
//     };

//     // Next button
//     document.getElementById('nextButton').onclick = () => {
//         player.nextTrack().then(() => {
//             console.log('Skipped to next track!');
//         });
//     };

//     // Previous button
//     document.getElementById('prevButton').onclick = () => {
//         player.previousTrack().then(() => {
//             console.log('Skipped to previous track!');
//         });
//     };
// };


// //検索した楽曲情報の取得して再生
// function playTrack(trackUri) {
//     const deviceId = localStorage.getItem('device_id');
//     const accessToken = "{{ access_token }}"; // サーバー側から渡されたアクセストークン

//     // Spotify APIに対して再生リクエストを送信
//     fetch(`https://api.spotify.com/v1/me/player/play?device_id=${deviceId}`, {
//         method: 'PUT',
//         body: JSON.stringify({ uris: [trackUri] }),
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${accessToken}`
//         },
//     })
//     .then(response => {
//         if (response.ok) {
//             console.log('Track is playing');
//         } else {
//             console.error('Failed to play track', response);
//         }   
//     })
//     .catch(error => {
//         console.error('Error playing track:', error);
//     });
// }

// //検索結果をクリックして再生するための例
// document.getElementById('trackButton').onclick = function(event) {
//     const trackUri = document.getElementById('trackUriInput').value;
//     playTrack(trackUri);  // 取得したURIをplayTrackに渡して再生
// };

// // 検索結果をクリックして再生するためのイベントリスナー
// // document.querySelectorAll('.trackButton').forEach(button => {
// //     button.addEventListener('click', function() {
// //         const trackUri = this.getAttribute('data-uri');
// //         playTrack(trackUri);  // 取得したURIをplayTrackに渡して再生
// //     });
// // });


window.onSpotifyWebPlaybackSDKReady = () => {
    //const token = '[My access token]';
    const token = "{{ access_token }}";
    const player = new Spotify.Player({
        name: 'Web Playback SDK Quick Start Player',
        getOAuthToken: cb => { cb(token); },
        volume: 0.5
    });

    // Ready
    player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
    });

    // Not Ready
    player.addListener('not_ready', ({ device_id }) => {
        console.log('Device ID has gone offline', device_id);
    });

    player.addListener('initialization_error', ({ message }) => {
        console.error(message);
    });

    player.addListener('authentication_error', ({ message }) => {
        console.error(message);
    });

    player.addListener('account_error', ({ message }) => {
        console.error(message);
    });

    document.getElementById('togglePlay').onclick = function() {
      player.togglePlay();
    };

    player.connect();
}
