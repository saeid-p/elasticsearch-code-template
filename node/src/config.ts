import process from "process";

const readEnvironmentVariable = (key: string, defaultValue?: string) => process.env[key] ?? defaultValue;

export { readEnvironmentVariable };
