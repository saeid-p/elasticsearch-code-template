const messageResponse = "Hello world!";

/** Returns a mock message. */
export const getMessage = () => messageResponse;

/** Prints a message using a printer service passed to the function. */
export const printService = (printer, message) => printer(message);
