export function before(user, photo) {
  return user !== null;
}

export function after(user, photo) {
  return user !== null && user.id === photo.ownerId;
}
