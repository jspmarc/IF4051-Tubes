export function getPassword() {
  const password = document.cookie
    .split("; ")
    .find((c) => c.startsWith("password="))
    ?.split("=")[1];

  return !password ? null : password;
}

export function savePassword(password: string) {
  document.cookie = `password=${password}; samesite=strict; max-age=3600`; // 1 hour max age
}

export default {
  getPassword,
  savePassword,
};
