const config = state => state.app.config
const palette = state => state.app.config.palette
const isLoading = state => state.app.isLoading
const isLoggedIn = state => state.app.isLoggedIn
const user = state => state.app.user

export {
  config,
  palette,
  isLoading,
  isLoggedIn,
  user,
}
