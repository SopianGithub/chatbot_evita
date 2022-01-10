import axios from 'axios'

const state = {
  sidebar: {
    opened: false,
  },
  config: {
    palette: {
      primary: '#4ae387',
      danger: '#e34a4a',
      info: '#4ab2e3',
      success: '#db76df',
      warning: '#f7cc36',
      white: '#fff',
      black: '#000',
      fontColor: '#34495e',
      transparent: 'transparent',
      lighterGray: '#ddd',
    },
  },
  isLoading: true,
  isLoggedIn: false,
  user: null,
  msgNotification: '',
}

const mutations = {
  setLoading (state, isLoading) {
    state.isLoading = isLoading
  },
  set_user (state, data) {
    state.user = data
    state.isLoggedIn = true
  },
  set_notif (state, message) {
    state.msgNotification = message
  },
  reset_notif (state) {
    state.msgNotification = null
  },
  reset_user (state) {
    state.user = null
    state.isLoggedIn = false
  },
}

const actions = {
  login ({ dispatch, commit }, data) {
    return new Promise((resolve, reject) => {
      axios.post('http://localhost:5000/login', data)
        .then(response => {
          if (response.data.message == 'Login Success') {
            const nik = response.data.values.users.nik
            localStorage.setItem('nik', nik)
            // setHeaderToken(token)
            // dispatch('get_user')
            commit('set_user', response.data.values.users)
            resolve(response)
          } else {
            reject(response.data.message)
          }
        })
        .catch(err => {
          commit('reset_user')
          localStorage.removeItem('nik')
          reject(err)
        })
    })
  },
  async get_user ({ commit }) {
    if (!localStorage.getItem('nik')) {
      return
    }
    try {
      const response = await axios.get(`http://127.0.0.1:5000/login/${localStorage.getItem('nik')}`)
      commit('set_user', response.data.values)
    } catch (error) {
      commit('reset_user')
      // removeHeaderToken()
      localStorage.removeItem('nik')
      return error
    }
  },
  logout ({ commit }) {
    return new Promise((resolve) => {
      commit('reset_user')
      localStorage.removeItem('nik')
      // removeHeaderToken()
      resolve()
    })
  },
}

export default {
  state,
  mutations,
  actions,
}
